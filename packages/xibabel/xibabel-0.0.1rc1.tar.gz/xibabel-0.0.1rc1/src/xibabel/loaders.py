""" Load various data formats into xibabel images
"""

from functools import partial
from pathlib import Path
import json
import logging
import importlib
import os.path as op

import numpy as np
import psutil

import nibabel as nib
from nibabel.spatialimages import HeaderDataError
from nibabel.filename_parser import parse_filename
from nibabel.fileholders import FileHolder
from nibabel.affines import from_matvec, apply_affine

import fsspec
import xarray as xr
import dask.array as da

from .xutils import merge


logger = logging.getLogger(__name__)


def max_available_div(div=10):
    """ Set default chunk as fraction of maximum aailable memory
    """
    return psutil.virtual_memory().available / div


MAXCHUNK_STRATEGY = max_available_div


class FDataObj:
    """ Wrapper for dataobj that returns floating point values from indexing.
    """

    # Signal that this is a proxy (for a proxy).
    is_proxy = True

    def __init__(self, dataobj, dtype=np.float64):
        dtype = np.dtype(dtype)
        if not issubclass(dtype.type, np.inexact):
            raise ValueError(f'{dtype} should be floating point type')
        self._dataobj = dataobj
        self.dtype = dtype
        self.shape = dataobj.shape
        self.ndim = dataobj.ndim
        self.order = getattr(dataobj, 'order', None)

    def __getitem__(self, slicer):
        """ Return image data as floating point type ``self.dtype``.
        """
        return np.asanyarray(self._dataobj[slicer], dtype=self.dtype)

    def chunk_sizes(self, maxchunk=None):
        """ Calculate chunk sizes for dataobj shape

        Parameters
        ----------
        maxchunk : None or int, optional
            The largest allowable chunk sizes in bytes.

        Returns
        -------
        chunk_sizes : list
            Chunk sizes for Dask array creation, being number of elements in
            one chunk over all axes of array in ``self.dataobj``.
        """
        return default_chunks(self, maxchunk)

    def reshape(self, shape):
        """ Return object reshaped to `shape`

        Notes
        -----
        There is no requirement that the contained ``dataobj`` has a
        ``reshape`` method; if not, calling this method will raise an
        ``AttributeError``.
        """
        return self.__class__(self._dataobj.reshape(shape), self.dtype)


def default_chunks(arr, order=None, maxchunk=None):
    """ Calculate chunk sizes for array-like `arr` from shape and `order`.

    Parameters
    ----------
    arr : array-like
        Object with attributes `.shape` and `.dtype`.  It can also have
        attribute `order`, and / or `.flags.f_contiguous`, used only if `order`
        below is None.
    order : {None, "F", "C"}
        Memory ordering of array.
    maxchunk : None or int, optional
        The largest allowable chunk sizes in bytes.

    Returns
    -------
    chunk_sizes : list
        Chunk sizes for Dask array creation, being number of elements in
        one chunk over all axes of array in ``self.dataobj``.
    """
    if order is None:  # FDataObj, dataobj
        order = getattr(arr, 'order', None)  # FDataObj, dataobj
    if order is None:  # ndarray
        order = getattr(getattr(arr, 'flags', None), 'f_contiguous', 'C')
    ndim = len(arr.shape)
    sizes = [None] * ndim
    if maxchunk is None:
        maxchunk = MAXCHUNK_STRATEGY()
    chunk_size = np.prod(arr.shape) * arr.dtype.itemsize
    if chunk_size <= maxchunk:
        return sizes
    axis_nos = range(ndim)
    if order == 'F':
        axis_nos = axis_nos[::-1]
    for axis_no in axis_nos:
        chunk_size //= arr.shape[axis_no]
        n_chunks = maxchunk // chunk_size
        if n_chunks:
            sizes[axis_no] = int(n_chunks)
            return sizes
        sizes[axis_no] = 1
    return sizes


_DIMNO2NAME = {
    None: None,
    0: 'i',
    1: 'j',
    2: 'k'}


_DIMNAME2NO = {v: k for k, v in _DIMNO2NAME.items()}


_TIME_UNIT_SCALER = {
    'sec': 1,
    'msec': 1 / 1000,
    'usec': 1 / 1_000_000}


class NiHeader2Attrs:

    def __init__(self, header):
        self.header = nib.Nifti1Header.from_header(header)

    def get_dim_labels(self):
        freq_dim, phase_dim, slice_dim = self.header.get_dim_info()
        return {'xib-FrequencyEncodingDirection': _DIMNO2NAME[freq_dim],
                'PhaseEncodingDirection': _DIMNO2NAME[phase_dim],
                'SliceEncodingDirection': _DIMNO2NAME[slice_dim]}

    def get_slice_timing(self):
        hdr = self.header
        freq_dim, phase_dim, slice_dim = hdr.get_dim_info()
        if not slice_dim:
            return None
        duration = hdr.get_slice_duration()
        if duration == 0:
            return None
        slice_start, slice_end = hdr['slice_start'], hdr['slice_end']
        n_slices = hdr.get_n_slices()
        if slice_start != 0 or slice_end != n_slices - 1:
            return None
        try:
            return list(hdr.get_slice_times())
        except HeaderDataError:
            return None

    def get_repetition_time(self):
        hdr = self.header
        zooms = hdr.get_zooms()
        if len(zooms) < 4:
            return None
        time_zoom = zooms[3]
        space_units, time_units = hdr.get_xyzt_units()
        if time_units == 'unknown':
            return None
        return _TIME_UNIT_SCALER[time_units] * time_zoom

    def get_affines(self):
        """ Collect valid affines
        """
        hdr = self.header
        affines = {}
        for affine_type in 'qform', 'sform':
            code = hdr.get_value_label(affine_type + '_code')
            if code != 'unknown':
                affine = getattr(hdr, 'get_' + affine_type)()
                affines[code] = affine.tolist()
        return affines

    def to_attrs(self):
        attrs = self.get_dim_labels()
        attrs['SliceTiming'] = self.get_slice_timing()
        attrs['RepetitionTime'] = self.get_repetition_time()
        attrs['xib-affines'] = self.get_affines()
        return {k: v for k, v in attrs.items() if v is not None}


class Attrs2NiHeader:
    """ Class writes BIDS attribute dictionary into NIfTI header.
    """

    def __init__(self, header=None, attrs=None):
        self.header = nib.Nifti1Header.from_header(header)
        self.attrs = {} if attrs is None else attrs.copy()

    def set_dim_labels(self):
        # Assume canonical axis order.
        d = self.attrs
        self.header.set_dim_info(
            freq=_DIMNAME2NO.get(d.get('xib-FrequencyEncodingDirection')),
            phase=_DIMNAME2NO.get(d.get('PhaseEncodingDirection')),
            slice=_DIMNAME2NO.get(d.get('SliceEncodingDirection')))

    def set_slice_timing(self):
        slice_times = self.attrs.get('SliceTiming')
        if slice_times is None:
            return
        try:
            return self.header.set_slice_times(slice_times)
        except HeaderDataError:
            pass

    def set_repetition_time(self):
        hdr = self.header
        zooms = np.array(hdr.get_zooms())
        # Assume header record of image already has correct shape.
        if len(zooms) < 4:
            return
        TR = self.attrs.get('RepetitionTime')
        TR, units = (0, None) if TR is None else (TR, 'sec')
        zooms[3] = TR
        hdr.set_xyzt_units(t=units)
        hdr.set_zooms(zooms)

    def set_affines(self):
        """ Set valid affines to header.
        """
        hdr = self.header
        affines = self.attrs.get('xib-affines', {})
        methods = [hdr.set_sform, hdr.set_qform]
        for code in ('mni', 'talairach', 'template', 'aligned', 'scanner'):
            if code in affines:
                methods.pop()(affines[code], code)
                if not methods:
                    break

    def updated_header(self):
        self.set_dim_labels()
        self.set_slice_timing()
        self.set_affines()
        self.set_repetition_time()
        return self.header


def hdr2attrs(header):
    # We could try extracting more information from other file types, but
    return NiHeader2Attrs(header).to_attrs()


def load_zarr(url_or_path, **kwargs):
    r""" Load image from Zarr/Xibabel-format data at `url_or_path`

    Parameters
    ----------
    url_or_path : str or Path
    \*\*kwargs : dict
        Any remaining named arguments passed to `xr.open_dataarray`.

    Returns
    -------
    ximg : Xibabel image

    Raises
    ------
    XibFileError
        If there is no file corresponding to `url_or_path`.
    """
    return xr.open_dataarray(url_or_path,
                             engine='zarr',
                             chunks='auto',
                             **kwargs)


class XibError(Exception):
    """ Errors from Xibabel file inference and operations
    """


class XibFormatError(XibError):
    """ Errors from Xibabel format specification or inference
    """


class XibFileError(XibError):
    """ Error from Xibabel file operations
    """


_JSON_MARKER = '__json__'


def _json_attrs2attrs(attrs):
    """ Read JSON formed for encoding nested structures to netCDF
    """
    out = {}
    for key, value in attrs.items():
        if (isinstance(value, list) and
            len(value) == 2 and
            value[0] == _JSON_MARKER):
            value = json.loads(value[1])
        out[key] = value
    return out


def _1d_arrayable(v):
    try:
        arr = np.array(v)
    except ValueError:
        return False
    return arr.ndim < 2


class NPEncoder(json.JSONEncoder):

    def default(self, obj):
        if hasattr(obj, 'tolist'):
            return obj.tolist()
        # No supported serialization, pass to default encoder to raise.
        return super().default(obj)


_jdumps = partial(json.dumps, cls=NPEncoder)


def _attrs2json_attrs(attrs):
    """ Write JSON formed for encoding nested structures to netCDF
    """
    out = {}
    for key, value in attrs.items():
        if (isinstance(value, dict) or
            (isinstance(value, (list, tuple)) and not _1d_arrayable(value))):
            value = [_JSON_MARKER, _jdumps(value)]
        out[key] = value
    return out


def _check_netcdf():
    if importlib.util.find_spec('h5netcdf') is None:
        raise XibFileError('Please install h5netcdf module to load netCDF')


def load_netcdf(url_or_path, **kwargs):
    r""" Load image from netCDF/Xibabel-format data at `url_or_path`

    Parameters
    ----------
    url_or_path : str or Path
    \*\*kwargs : dict
        Any remaining named arguments passed to `xr.open_dataarray`.

    Returns
    -------
    ximg : Xibabel image

    Raises
    ------
    XibFileError
        If there is no file corresponding to `url_or_path`.
    """
    _check_netcdf()
    with fsspec.open(url_or_path) as fobj:
        img = xr.open_dataarray(fobj, engine='h5netcdf', **kwargs)
    img.attrs = _json_attrs2attrs(img.attrs)
    return img


def load(url_or_path, *, format=None, **kwargs):
    r""" Load image Xibabel or Nibbel image at `url_or_path`

    Parameters
    ----------
    url_or_path : str or Path
    format : None or str, optional
        If None, infer format from `url_or_path`, otherwise one of
        {', '.join(f'{e}' for e in PROCESSORS.format_processors)}
    \*\*kwargs : dict
        Any remaining named arguments passed to backend corresponding to
        `format`.

    Returns
    -------
    ximg : Xibabel image

    Raises
    ------
    XibFileError
        If there is no file corresponding to `url_or_path`.
    """
    if format is None:
        format = PROCESSORS.guess_format(url_or_path)
    return PROCESSORS.get_loader(format)(url_or_path, **kwargs)


# Extensions we will search for valid images paired with JSON files.
_JSON_PAIRED_EXTS = ('.nii.gz', '.nii')


def drop_suffix(in_path, suffix):
    """ Drop suffix in `suffixes` from str or ``Path`` `in_path`

    `suffix` can be ``str`` (suffix to drop) or sequence.  If sequence, drops
    first matching suffix in sequence `suffix`.

    Parameters
    ----------
    in_path : str or Path
        Path from which to drop suffix.
    suffix : str or sequence
        If ``str``, suffix to drop.  If sequence, search for each suffix, and
        drop first found suffix from `in_path`.

    Returns
    -------
    out_path : str or Path
        Return type matches that of `in_path`.
    """
    if not hasattr(in_path, 'is_file'):
        return _drop_suffix_str(in_path, suffix)
    return in_path.with_name(_drop_suffix_str(in_path.name, suffix))


def _drop_suffix_str(path_str, suffix):
    suffixes = (suffix,) if isinstance(suffix, str) else suffix
    for suffix in suffixes:
        if path_str.endswith(suffix):
            return path_str[:-(len(suffix))]
    return path_str


def replace_suffix(in_path, old_suffix, new_suffix):
    """ Replace `in_path` suffix with `new_suffix`, allowing for `old_suffix`

    Always replace suffix of `in_path`, if present, but allowing for any
    special (multi-dot) suffixes in `old_sequence`.

    `old_suffix` can be ``str`` (suffix to drop) or sequence.  If sequence,
    drops first matching suffix in sequence `suffixes` before appending
    `new_suffix`.

    Parameters
    ----------
    in_path : str or Path
        Path from which to replace suffix.
    old_suffix : str or sequence
        If ``str``, suffix to drop before replacing.  If sequence, search for
        each suffix, and drop first found suffix from `in_path`.
    new_suffix : str
        Suffix to append.

    Returns
    -------
    out_path : str or Path
        Return type matches that of `in_path`.
    """
    is_path = hasattr(in_path, 'is_file')
    path_str = in_path.name if is_path else in_path
    dropped = _drop_suffix_str(path_str, old_suffix)
    replaced = op.splitext(dropped)[0] + new_suffix
    return in_path.with_name(replaced) if is_path else replaced


def _valid_or_raise(fs, url_base, exts):
    for ext in exts:
        target_url = replace_suffix(url_base, (), ext)
        if fs.exists(target_url):
            return fsspec.open(target_url, compression='infer')
    msg_suffix = (('one of ' if len(exts) > 1 else '') +
                  ', '.join(f"'{e}'" for e in exts))
    raise XibFileError(
        f"No valid file matching '{url_base}' + {msg_suffix}")


def load_bids(url_or_path, *, require_json=True, **kwargs):
    r""" Load image from BIDS-format data at `url_or_path`

    `url_or_path` may point directly to ``.json`` file, or to Nibabel format
    file, for which we expect a ``.json`` file to be present.

    In the second case, if `require_json` is True, and we cannot find a
    matching `.json` file, raise error, otherwise return image as best read.

    Parameters
    ----------
    url_or_path : str or Path
    require_json : {True, False}, optional, keyword-only
        If True, raise error if `url_or_path` is an image, and there is no
        matching JSON file.
    \*\*kwargs : dict
        Any remaining named arguments passed to `fsspec.open`.

    Returns
    -------
    bids_ximg : Xibabel image

    Raises
    ------
    XibFileError
        If `require_json` is True, `url_or_path` does not name a ``.json`` file
        and there is no ``.json`` file corresponding to `url_or_path`.
    """
    sidecar_file = None
    # If url_or_path has .json suffix, search for matching image file.
    if str(url_or_path).endswith('.json'):
        sidecar_file = fsspec.open(url_or_path, **kwargs)
        fs = sidecar_file.fs
        if not fs.exists(url_or_path):
            raise XibFileError(
                f'{url_or_path} does not appear to exist')
        img_file = _valid_or_raise(fs,
                                   drop_suffix(url_or_path, '.json'),
                                   _JSON_PAIRED_EXTS)
    else:  # Image file extensions.  Search for JSON.
        img_file = fsspec.open(url_or_path, compression='infer', **kwargs)
        fs = img_file.fs
        if not fs.exists(url_or_path):
            raise XibFileError(
                f'{url_or_path} does not appear to exist')
        url_uncomp = drop_suffix(url_or_path, _comp_exts())
        url_json = replace_suffix(url_uncomp, (), '.json')
        if fs.exists(url_json):
            sidecar_file = fs.open(url_json)
        elif require_json:
            raise XibFileError(
                f'BIDS loading {url_or_path} but no corresponding '
                f'{url_json} file, and `require_json` is True')
    nib_img, attrs = _nibabel2img_attrs(img_file)
    if sidecar_file:
        with sidecar_file as fobj:
            attrs.update(json.load(fobj))
    return _img_attrs2ximg(
        nib_img,
        **{'attrs': attrs, 'name': _url2name(url_or_path)})


def load_nibabel(url_or_path, **kwargs):
    r""" Load image from Nibabel-format data at `url_or_path`

    `url_or_path` may point directly to ``.json`` file, or to Nibabel format
    file, for expect a ``.json`` file to be present, in which case we will load
    it.

    Parameters
    ----------
    url_or_path : str or Path
    \*\*kwargs : dict
        Any remaining named arguments passed to `fsspec.open`.

    Returns
    -------
    ximg : Xibabel image

    Raises
    ------
    XibFileError
        If there is no file corresponding to `url_or_path`.
    """
    return load_bids(url_or_path, require_json=False, **kwargs)


def from_array(arr, *, fa_kwargs=None, **kwargs):
    r""" Create image from array-like `arr`

    Assume array dimensions correspond to NIfTI labels.

    Parameters
    ----------
    arr : array-like
    chunks : 'auto' or int or tuple
        See documentation for ``dask.array.from_array``
    fa_kwargs : None or mapping, optional, keyword only
        Keyword arguments that we pass through the ``dask.array.from_array``
        function.
    \*\*kwargs : mapping, keyword arguments
        Keyword arguments to pass to ``DataArray`` constructor.  A common
        example is ``dims`` (None or sequence of dimension names).  If None,
        use NIfTI convention for coordinate names.  If sequence, it must match
        the number of dimensions of `arr`.

    Returns
    -------
    ximg : Xibabel image
    """
    arr_like = FDataObj(arr) if nib.is_proxy(arr) else arr
    ximg = _arr_attrs2ximg(arr_like, fa_kwargs=fa_kwargs, **kwargs)
    if 'dims' not in kwargs:  # Use NIfTI conventions
        ximg = _squeeze_time(ximg)
    return ximg


def _comp_exts():
    return tuple(f'.{ext}' for ext in fsspec.utils.compressions)


def _path2class(filename):
    compression_exts = _comp_exts()
    for klass in nib.all_image_classes:
        if len(klass.files_types) > 1:
            continue
        base, ext, gzext, ftype = parse_filename(filename,
                                                 klass.files_types,
                                                 compression_exts)
        if ftype == 'image':
            return klass
    raise XibFileError(f'No single-file Nibabel class for {filename}')


class FSFileHolder(FileHolder):

    def __del__(self):
        self.fileobj.close()


_NI_DIM_NAMES = ('i', 'j', 'k', 'time', 'p', 'q', 'r')
_NI_SPACE_DIMS = _NI_DIM_NAMES[:3]
_NI_TIME_DIM = _NI_DIM_NAMES[3]


def _nibabel2img_attrs(img_file):
    # Identify relevant files from img_file
    # Make file_map with opened files.
    if 'local' in img_file.fs.protocol:
        img = nib.load(img_file.path)
    else:  # Not local - use stream interface.
        img_klass = _path2class(img_file.path)
        # We are passing out opened fsspec files.
        fh = FileHolder(img_file.path, img_file.open())
        img = img_klass.from_file_map({'image': fh})
    return img, hdr2attrs(img.header)


def _img_attrs2ximg(obj, *, fa_kwargs=None, **kwargs):
    arr_like = FDataObj(obj.dataobj)
    fa_kwargs = {} if fa_kwargs is None else {}
    if not fa_kwargs.get('fancy'):  # Assume no fancy indexing by default.
        fa_kwargs['fancy'] = False
    if not fa_kwargs.get('chunks'):
        fa_kwargs['chunks'] = arr_like.chunk_sizes()
    ximg = _arr_attrs2ximg(arr_like,
                           fa_kwargs=fa_kwargs,
                           **kwargs)
    return _squeeze_time(ximg) if hasattr(obj, 'get_sform') else ximg


def _squeeze_time(ximg):
    # https://nifti.nimh.nih.gov/nifti-1/documentation/nifti1fields/nifti1fields_pages/dim.html
    # > If dim[4]=1 or dim[0] < 4, there is no time axis.
    if 'time' in ximg.dims and len(ximg['time']) == 1:
        ximg = ximg.sel(time=0)
    return ximg


def _arr_attrs2ximg(arr, *, fa_kwargs=None, **kwargs):
    fa_kwargs = {} if fa_kwargs is None else fa_kwargs
    if not fa_kwargs.get('chunks'):
        fa_kwargs['chunks'] = default_chunks(arr)
    shape = arr.shape
    if not kwargs.get('dims'):
        kwargs['dims'] = list(_NI_DIM_NAMES)[:len(shape)]
    kwargs['coords'] = _filled_coords(kwargs.get('coords', {}),
                                      kwargs['dims'],
                                      shape,
                                      kwargs.get('attrs', {}))
    return xr.DataArray(da.from_array(arr, **fa_kwargs), **kwargs)


def _filled_coords(coords, dims, shape, attrs):
    # Fill space coordinate axes
    out_coords = coords.copy()
    for ax_no, ax_name in enumerate(dims):
        if ax_name not in _NI_SPACE_DIMS or ax_name in out_coords:
            continue
        out_coords[ax_name] = xr.DataArray(
            np.arange(shape[ax_no]),
            dims=[ax_name])
    if _NI_TIME_DIM not in dims:
        return out_coords
    # Consider special cases for: hz, ppm, rad
    # https://nifti.nimh.nih.gov/nifti-1/documentation/nifti1fields/nifti1fields_pages/xyzt_units.html
    # Maybe set attrs['xib-time-unts'] from header, and use here.
    TR = attrs.get("RepetitionTime")
    if not TR:
        return out_coords
    # Add time axis coordinates.
    n_time = shape[dims.index(_NI_TIME_DIM)]
    out_coords[_NI_TIME_DIM] = xr.DataArray(
        np.arange(0, n_time) * TR,
        dims=[_NI_TIME_DIM],
        attrs={"units": "s"})
    return out_coords


def _url2name(url_or_path):
    name = drop_suffix(url_or_path, _comp_exts())
    return Path(name).stem


def save(obj, url_or_path, format=None, **kwargs):
    r""" Save Xibabel image at `url_or_path`

    Parameters
    ----------
    url_or_path : str or Path
    format : None or str, optional
        If None, infer format from `url_or_path`, otherwise one of
        'zarr', 'netcdf', 'bids', 'nibabel'.
    \*\*kwargs : dict
        Any remaining named arguments passed to backend corresponding to
        `format`.

    Returns
    -------
    ret : object
        Return depends on `format`.  See `save_zarr` and `save_netcdf` for
        examples.
    """
    if format is None:
        format = PROCESSORS.guess_format(url_or_path)
    return PROCESSORS.get_saver(format)(obj, url_or_path, **kwargs)


def save_zarr(obj, url_or_path, **kwargs):
    r""" Save Xibabel image at `url_or_path` in Zarr / Xibabel format.

    Parameters
    ----------
    url_or_path : str or Path
    \*\*kwargs : dict
        Arguments to pass to `to_zarr` method of `obj`.

    Returns
    -------
    zbe : ZarrBackendStore
    """
    return obj.to_zarr(url_or_path, mode='w', **kwargs)


def save_netcdf(obj, url_or_path, **kwargs):
    r""" Save Xibabel image at `url_or_path` in netCDF / Xibabel format.

    Parameters
    ----------
    url_or_path : str or Path
    \*\*kwargs : dict
        Arguments to pass to `to_netcdf` method of `obj`.

    Returns
    -------
    None
    """
    _check_netcdf()
    out = obj.copy()  # Shallow copy by default.
    out.attrs = _attrs2json_attrs(out.attrs)
    return out.to_netcdf(url_or_path, engine='h5netcdf', **kwargs)


def save_bids(obj, url_or_path, **kwargs):
    r""" Save Xibabel image at `url_or_path` as NIfTI / BIDS JSON

    Parameters
    ----------
    url_or_path : str or Path
    \*\*kwargs : dict
        Any remaining named arguments passed to `fsspec.open`.

    Returns
    -------
    None
    """
    nib_img, attrs = to_nifti(obj)
    if str(url_or_path).endswith('.json'):
        json_uop = url_or_path
        img_uop = replace_suffix(url_or_path, '.json', '.nii.gz')
    else:
        img_uop = url_or_path
        json_uop = replace_suffix(
            drop_suffix(url_or_path, _comp_exts()),
            (),
            '.json')
    img_file = fsspec.open(img_uop, compression='infer', **kwargs)
    sidecar_kwargs = merge(kwargs, {'mode': 'wt'})
    sidecar_file = img_file.fs.open(json_uop, **sidecar_kwargs)
    with sidecar_file as f:
        f.write(_jdumps(attrs))
    if 'local' in img_file.fs.protocol:
        nib.save(nib_img, img_file.path)
        return
    # Not local - use stream interface.
    img_klass = _path2class(img_uop.path)
    # We are passing out opened fsspec files.
    with img_uop as fh:
        img_klass.to_file_map({'image': fh})


class Processors:

    format_processors = {
        'zarr': dict(exts=('ximg',),
                     loader=load_zarr,
                     saver=save_zarr),
        'netcdf': dict(exts=('nc',),
                     loader=load_netcdf,
                     saver=save_netcdf),
        'bids': dict(exts=('json',),
                     loader=load_bids,
                     saver=save_bids),
        'nibabel': dict(exts=(),  # Defer to Nibabel for extensions
                     loader=load_nibabel,
                     saver=save_bids),
    }

    def __init__(self):
        self.loaders = set()
        self.savers = set()
        self.ext2fmt = {}
        for fmt, info in self.format_processors.items():
            if info['loader']:
                self.loaders.add(fmt)
            if info['saver']:
                self.savers.add(fmt)
            for ext in info['exts']:
                self.ext2fmt[ext] = fmt

    def get_loader(self, fmt):
        return self.get_processor(fmt, 'loader')

    def get_saver(self, fmt):
        return self.get_processor(fmt, 'saver')

    def get_processor(self, fmt, ptype='loader'):
        fmt = 'nibabel' if fmt is None else fmt
        pset = (self.loaders if ptype == 'loader'
                else self.savers)
        if fmt not in pset:
            raise XibFormatError(
                f"Cannot use format '{fmt}' as {ptype} for image; "
                f"valid formats are {','.join(pset)}")
        return self.format_processors[fmt][ptype]

    def guess_format(self, file_path):
        suff = str(file_path).split('.')[-1]
        return self.ext2fmt.get(suff)


PROCESSORS = Processors()


def _ni_sort_expand_dims(img_dims):
    # Allow for 3D images
    target_dims = _NI_SPACE_DIMS
    if not set(img_dims).issubset(_NI_SPACE_DIMS):
        target_dims += (_NI_TIME_DIM,)
    x_dims = []
    x_axes = []
    out_order = []
    for expected_pos, expected_dim in enumerate(target_dims):
        try:
            curr_pos = img_dims.index(expected_dim)
        except ValueError:
            x_dims.append(expected_dim)
            x_axes.append(expected_pos)
            continue
        out_order.append(img_dims[curr_pos])
    return (out_order + [d for d in img_dims if d not in out_order],
            x_dims,
            x_axes)


def to_nifti(ximg):
    # Reorient, expand missing dimensions
    order, dims, axes = _ni_sort_expand_dims(ximg.dims)
    ximg = ximg.transpose(*order).expand_dims(dims, axes)
    # Adjust affines to current state of ximg.
    back = ximg.xi.with_updated_affines()
    # Build preliminary header.
    hdr = nib.Nifti1Header()
    hdr.set_data_shape(back.shape)
    # Build header from attributes.
    hdr = Attrs2NiHeader(hdr, back.attrs).updated_header()
    return nib.Nifti1Image(back, None, hdr), back.attrs


@xr.register_dataarray_accessor("xi")
class XiAccessor:

    def __init__(self, xarray_obj):
        self._obj = xarray_obj

    def get_affines(self):
        """ Get spatial affines from attributes of image

        Returns
        -------
        affines : dict
            Dictionary with key, value pairs where key is string giving space
            to which affine maps, and values are 4x4 spatial affine arrays.

        Notes
        -----
        Returned `affines` are copies; if you modify the arrays in `affines`,
        this will not affect the original image.
        """
        aff_d = self._obj.attrs.get('xib-affines', {})
        return {space: np.array(aff) for space, aff in aff_d.items()}

    def set_affines(self, affines):
        """ Set spatial affines to attributes of image

        Affines overwrite existing affines.  If the affine does not exist, we
        append to the affines dictionary.

        Parameters
        ----------
        affines : dict
            Dictionary where key, value pairs are affine space name and 4x4
            affine array, respectively.

        Notes
        -----
        Set `affines` are copies; if you modify the arrays in `affines`,
        this will not affect the image affines.  The set affines overwrite
        correspnding existing affines.
        """
        aff_d = self._obj.attrs.get('xib-affines', {})
        for space, aff in affines.items():
            aff_d[space] = np.array(aff)
        self._obj.attrs['xib-affines'] = aff_d

    def with_updated_affines(self):
        """ Return image with affines, coordinates updated to match state.

        Return image `adj_img` where the affines and coordinates correctly
        reflect any detected slicing of the original image.

        Returns
        -------
        adj_img : Xibabel image
            Image with adjusted affines, and for which spatial coordinate
            indices have been reset to sequential 0-based default.

        Notes
        -----
        The affines and i, j, k coordinates reflect the state of the image as
        of the last call to this function, or as of image load.

        The affines are always 4x4, and always refer to i, j, k space,
        regardless of dimension ordering, and of the presence of i, j, k
        dimensions.
        """
        adj_img = self._obj.copy()
        assert adj_img.attrs is not self._obj.attrs
        out_affines = {}
        for space, affine in self.get_affines().items():
            out_affines[space] = self._adjusted_affine(affine, adj_img.coords)
        adj_img.attrs['xib-affines'] = out_affines
        return adj_img.xi._with_reset_coordinates()

    def _adjusted_affine(self, affine, coords):
        vox_origin = np.zeros(3)
        vox_scalings = np.ones(3)
        for i, name in enumerate(_NI_SPACE_DIMS):
            vox_indices = np.ravel(coords.get(name, 0))
            vox_origin[i] = vox_indices[0]
            if len(vox_indices) > 1:
                vd = np.diff(vox_indices)
                if any(vd[1:] != vd[0]):
                    raise XibFormatError(
                        f'Cannot handle irregular voxel spacing for "{name}"')
                vox_scalings[i] = vd[0]
        return from_matvec(affine[:3, :3] * vox_scalings,
                           apply_affine(affine, vox_origin))

    def _with_reset_coordinates(self):
        ximg = self._obj
        coords = {}
        for name in _NI_SPACE_DIMS:
            if name not in ximg.dims:
                coords[name] = xr.DataArray(0)
                continue
            coords[name] = xr.DataArray(
                np.arange(ximg[name].shape[0]),
                dims=[name])
        return ximg.assign_coords(coords)
