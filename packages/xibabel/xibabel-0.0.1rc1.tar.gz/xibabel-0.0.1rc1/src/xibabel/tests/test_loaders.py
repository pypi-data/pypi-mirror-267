""" Test loaders
"""

from pathlib import Path
from copy import deepcopy
import os
from itertools import product, permutations
import json
import shutil

import numpy as np

import nibabel as nib

import xarray as xr

from xibabel import loaders
from xibabel.loaders import (FDataObj, load_bids, load_nibabel, load, save,
                             PROCESSORS, _json_attrs2attrs, drop_suffix,
                             replace_suffix, _attrs2json_attrs, hdr2attrs,
                             _path2class, XibFileError, XibFormatError,
                             to_nifti, _ni_sort_expand_dims, _NI_SPACE_DIMS,
                             _NI_TIME_DIM, _jdumps, from_array)
import nibabel.testing as nit
from xibabel.xutils import merge
from xibabel.testing import (JC_EG_FUNC, JC_EG_FUNC_JSON, JC_EG_ANAT,
                             JC_EG_ANAT_JSON, JH_EG_FUNC, skip_without_file,
                             fetcher, arr_dict_allclose)
from xibabel.tests.markers import h5netcdf_test

import pytest

rng = np.random.default_rng()


class FakeProxy:

    def __init__(self, array, order=None):
        self._array = array
        self.order = order
        self.ndim = array.ndim
        self.shape = array.shape

    def __getitem__(self, slicer):
        return self._array[slicer]

    def __array__(self):
        return self[:]

    def reshape(self, shape):
        return self._array.reshape(shape)


def test_fdataobj_basic():
    arr = np.arange(24).reshape((2, 3, 4))
    proxy = FakeProxy(arr)
    fproxy = FDataObj(proxy)
    assert fproxy.ndim == arr.ndim
    assert fproxy.shape == arr.shape
    assert fproxy.order is None
    assert np.all(fproxy[1, 2, :] == arr[1, 2, :])
    assert arr[1, 2, :].dtype == np.arange(2).dtype
    assert fproxy.dtype == np.dtype(np.float64)
    assert fproxy[1, 2, :].dtype == np.dtype(np.float64)
    fproxy = FDataObj(proxy, dtype=np.float32)
    assert fproxy.dtype == np.dtype(np.float32)
    with pytest.raises(ValueError, match='should be floating point type'):
        FDataObj(proxy, dtype=int)
    rprox = fproxy.reshape((6, 4))
    assert rprox.shape == (6, 4)
    assert np.all(rprox[:] == arr.reshape((6, 4)))


def test_chunking(monkeypatch):
    arr_shape = 10, 20, 30
    arr = rng.normal(size=arr_shape)
    fproxy = FDataObj(FakeProxy(arr))
    c_fproxy = FDataObj(FakeProxy(arr, order='C'))
    f_fproxy = FDataObj(FakeProxy(arr, order='F'))
    f64s = np.dtype(float).itemsize
    N = None
    for strategy, c_exp_sizes, f_exp_sizes in (
        (lambda : arr.size * f64s, [N, N, N], [N, N, N]),
        (lambda : arr.size * f64s - 1, [9, N, N], [N, N, 29]),
        (lambda : arr.size * f64s / 2 - 1, [4, N, N], [N, N, 14]),
        (lambda : arr.size * f64s / 10 - 1, [1, 19, N], [N, N, 2]),
        (lambda : arr.size * f64s / 30 - 1, [1, 6, N], [N, 19, 1]),
        (lambda : 11 * f64s, [1, 1, 11], [None, 1, 1]),
        (lambda : 10 * f64s, [1, 1, 10], [None, 1, 1]),
        (lambda : 2 * f64s, [1, 1, 2], [2, 1, 1]),
    ):
        monkeypatch.setattr(loaders, "MAXCHUNK_STRATEGY", strategy)
        assert fproxy.chunk_sizes() == c_exp_sizes
        assert c_fproxy.chunk_sizes() == c_exp_sizes
        assert f_fproxy.chunk_sizes() == f_exp_sizes


def out_back(img, out_path):
    if out_path.is_file():
        os.unlink(out_path)
    nib.save(img, out_path)
    img = nib.load(out_path)
    return img, hdr2attrs(img.header)


def out_back_xi(ximg, out_path):
    if out_path.is_file():
        os.unlink(out_path)
    save(ximg, out_path)
    # Compute on file to allow for later deletion of source file.
    return load(out_path).compute()


def test_nibabel_tr(tmp_path):
    # Default image.
    arr = np.zeros((2, 3, 4))
    img = nib.Nifti1Image(arr, np.eye(4), None)
    out_path = tmp_path / 'test.nii'
    back_img, attrs = out_back(img, out_path)
    exp_attrs = {'xib-affines': {'aligned': np.eye(4).tolist()}}
    assert attrs == exp_attrs
    arr = np.zeros((2, 3, 4, 6))
    img = nib.Nifti1Image(arr, np.eye(4), None)
    back_img, attrs = out_back(img, out_path)
    assert attrs == exp_attrs
    img.header.set_xyzt_units('mm', 'sec')
    back_img, attrs = out_back(img, out_path)
    exp_attrs.update({'RepetitionTime': 1.0})
    assert attrs == exp_attrs
    img.header.set_xyzt_units('mm', 'msec')
    back_img, attrs = out_back(img, out_path)
    assert attrs['RepetitionTime'] == 1 / 1000
    img.header.set_xyzt_units('mm', 'usec')
    back_img, attrs = out_back(img, out_path)
    assert attrs['RepetitionTime'] == 1 / 1_000_000


def test_nibabel_slice_timing(tmp_path):
    # Default image.
    arr = np.zeros((2, 3, 4, 5))
    img = nib.Nifti1Image(arr, np.eye(4), None)
    nib_path = tmp_path / 'test.nii'
    back_img, attrs = out_back(img, nib_path)
    # Check attrsdata.
    exp_attrs = {'xib-affines': {'aligned': np.eye(4).tolist()}}
    assert attrs == exp_attrs
    # Load ximg for comparison.
    ximg = load(nib_path).compute()  # Get data from file.
    assert ximg.attrs == exp_attrs
    # Try setting dimension information.
    img.header.set_dim_info(None, None, 1)
    nib_path2 = tmp_path / 'test2.nii'
    back_img, attrs = out_back(img, nib_path2)
    assert attrs == merge(exp_attrs, {'SliceEncodingDirection': 'j'})
    img.header.set_dim_info(1, 0, 2)
    back_img, attrs = out_back(img, nib_path2)
    exp_dim = merge(exp_attrs,
                    {'PhaseEncodingDirection': 'i',
                     'xib-FrequencyEncodingDirection': 'j',
                     'SliceEncodingDirection': 'k'})
    assert attrs == exp_dim
    img.header.set_slice_duration(1 / 4)
    back_img, attrs = out_back(img, nib_path2)
    assert attrs == exp_dim
    img.header['slice_start'] = 0
    back_img, attrs = out_back(img, nib_path2)
    assert attrs == exp_dim
    img.header['slice_end'] = 3
    back_img, attrs = out_back(img, nib_path2)
    assert attrs == exp_dim
    # Has time dimension.
    assert ximg.dims == tuple('ijk') + ('time',)
    # Check setting slice timing.
    img.header['slice_code'] = 4  # NIFTI_SLICE_ALT_DEC
    # This fills in the times.
    back_img, attrs = out_back(img, nib_path2)
    exp_timed = exp_dim.copy()
    slice_times = [0.75, 0.25, 0.5, 0]
    exp_timed['SliceTiming'] = slice_times
    assert attrs == exp_timed
    # Reset image back to default.
    back_ximg = out_back_xi(ximg, nib_path2)
    assert ximg.attrs == exp_attrs
    # Use header stuff to set slice timing.
    ximg.attrs['SliceTiming'] = slice_times
    back_ximg = out_back_xi(ximg, nib_path2)
    assert np.allclose(back_ximg.attrs['SliceTiming'], slice_times)


def _arr2ximg(arr, out_path):
    img = nib.Nifti1Image(arr, np.eye(4), None)
    nib.save(img, out_path)
    return load(out_path).compute()  # The file may later be deleted.


def test_nifti_load_save(tmp_path):
    # Default image.
    shape = (2, 3, 4, 5)
    arr = np.arange(np.prod(shape), dtype=float).reshape(shape)
    out_path = tmp_path / 'test.nii'
    ximg = _arr2ximg(arr, out_path)
    assert np.allclose(ximg, arr)
    assert ximg.dims == ('i', 'j', 'k', 'time')
    assert ximg.attrs.get('RepetitionTime') is None
    shape = (2, 3, 4, 5, 1)
    arr = np.arange(np.prod(shape), dtype=float).reshape(shape)
    out_path = tmp_path / 'test2.nii'
    ximg = _arr2ximg(arr, out_path)
    assert np.allclose(ximg, arr)
    assert ximg.dims == ('i', 'j', 'k', 'time', 'p')
    ximg.attrs['RepetitionTime'] = 2.0
    back_ximg = out_back_xi(ximg, tmp_path / 'test2a.nii')
    assert back_ximg.dims == ('i', 'j', 'k', 'time', 'p')
    assert back_ximg.attrs['RepetitionTime'] == 2.0
    shape = (2, 3, 4, 1, 5, 1)
    arr = np.arange(np.prod(shape), dtype=float).reshape(shape)
    out_path = tmp_path / 'test3.nii'
    ximg = _arr2ximg(arr, out_path)
    assert np.allclose(ximg, np.reshape(arr, (2, 3, 4, 5, 1)))
    assert ximg.dims == ('i', 'j', 'k', 'p', 'q')


@pytest.mark.parametrize("filename",
                         ('minc1_4d.mnc',
                          'minc2_4d.mnc',
                          'example_nifti2.nii.gz',
                          'phantom_varscale.PAR',
                         ))
def test_other_load(filename, tmp_path):
    in_path = nit.get_test_data() / filename
    nib_img = nib.load(in_path)
    ximg = load(in_path)
    assert nib_img.shape == ximg.shape
    assert len(ximg.dims) == len(nib_img.shape)
    assert np.allclose(nib_img.get_fdata(), ximg)


def test_from_array():
    # Without axis names, uses NIfTI convention
    a2d = rng.normal(size=(3, 4))
    ximg = from_array(a2d)
    assert ximg.dims == tuple('ij')
    assert np.all(a2d == ximg)
    a3d = rng.normal(size=(3, 4, 5))
    ximg = from_array(a3d)
    assert ximg.dims == tuple('ijk')
    assert np.all(a3d == ximg)
    a4d = rng.normal(size=(3, 4, 5, 6))
    ximg = from_array(a4d)
    assert ximg.dims == tuple('ijk') + ('time',)
    assert np.all(a4d == ximg)
    s5d = (3, 4, 5, 1, 6)
    a5d = rng.normal(size=s5d)
    ximg = from_array(a5d)
    assert ximg.dims == tuple('ijkp')
    assert np.all(a5d.reshape((3, 4, 5, 6)) == ximg)
    # With axis names, follows axis names.
    names = tuple('ji')
    ximg = from_array(a2d, dims=names)
    assert ximg.dims == names
    assert np.all(a2d == ximg)
    assert tuple(ximg.coords) == names
    names = tuple('pki')
    ximg = from_array(a3d, dims=names)
    assert ximg.dims == names
    # Only spatial axes have default coordinates.
    assert sorted(ximg.coords) == ['i', 'k']
    assert np.all(a3d == ximg)
    names = ('j', 'time', 'k', 'i')
    ximg = from_array(a4d, dims=names)
    assert ximg.dims == names
    assert sorted(ximg.coords) == ['i', 'j', 'k']
    assert np.all(a4d == ximg)
    # 5D with length 1 dimension not dropped by default.
    names = ('time',) + tuple('ikjn')
    ximg = from_array(a5d, dims=names)
    assert ximg.dims == names
    assert sorted(ximg.coords) == list('ijk')
    assert np.all(a5d == ximg)
    # With repetition time, we get a time axis
    attrs = {'RepetitionTime': 2.5}
    ximg = from_array(a5d, dims=names, attrs=attrs)
    assert ximg.dims == names
    assert sorted(ximg.coords) == ['i', 'j', 'k', 'time']
    assert np.all(a5d == ximg)
    assert np.all(ximg.coords['i'] == np.arange(4))
    assert np.all(ximg.coords['k'] == np.arange(5))
    # If you specify coordinates, we prefer the specified coordinates.
    coords = {'i': xr.DataArray(np.arange(2, 6), dims=['i'])}
    ximg = from_array(a5d, dims=names, attrs=attrs, coords=coords)
    assert np.all(ximg.coords['i'] == np.arange(2, 6))
    assert np.all(ximg.coords['k'] == np.arange(5))


def test_load_save_arr(tmp_path):
    out_path = tmp_path / 'test.nii'
    a3d = rng.normal(size=(3, 4, 5))
    ximg = from_array(a3d)
    assert ximg.xi.get_affines() == {}
    save(ximg, out_path)
    ximg_back = load(out_path)
    assert ximg_back.shape == (3, 4, 5)
    assert ximg_back.xi.get_affines() == {}


def test_get_set_affines():
    a3d = rng.normal(size=(3, 4, 5))
    ximg = from_array(a3d)
    assert ximg.dims == tuple('ijk')
    assert ximg.xi.get_affines() == {}
    new_affine = np.diag([1.2, 2.3, 3.4, 1])
    ximg.xi.set_affines({'scanner': new_affine})
    assert arr_dict_allclose(ximg.xi.get_affines(), {'scanner': new_affine})
    new_affine2 = new_affine.copy()
    new_affine2[:3, 3] = 10, 11, 12
    ximg.xi.set_affines({'scanner': new_affine2})
    assert arr_dict_allclose(ximg.xi.get_affines(),
                             {'scanner': new_affine2})
    ximg.xi.set_affines({'mni': new_affine})
    assert arr_dict_allclose(ximg.xi.get_affines(),
                             {'mni': new_affine, 'scanner': new_affine2})
    # Adjust affines gives the same reult back.
    ximg_adj = ximg.xi.with_updated_affines()
    assert arr_dict_allclose(ximg.xi.get_affines(),
                             {'mni': new_affine, 'scanner': new_affine2})
    # Coordinates with irregular spacing give affine errors.
    ximg_adj.coords['k'] = [0, 1, 3, 4, 5]
    with pytest.raises(XibFormatError,
                       match='Cannot handle irregular voxel spacing for "k"'):
        ximg_adj.xi.with_updated_affines()


def test_guess_format():
    root = Path('foo') / 'bar' / 'baz.suff'
    for v, exp in ((root, None),
                   (root.with_suffix('.nii'), None),
                   (root.with_suffix('.json'), 'bids'),
                   (root.with_suffix('.ximg'), 'zarr'),
                   (root.with_suffix('.nc'), 'netcdf'),
                   (root.with_suffix('.foo'), None)):

        assert PROCESSORS.guess_format(v) == exp
        assert PROCESSORS.guess_format(str(v)) == exp


def test__path2class():
    for url, exp_class in (
        ('/foo/bar/sub-07_T1w.nii.gz', nib.Nifti1Image),
        ('http://localhost:8999/sub-07_T1w.nii.gz', nib.Nifti1Image),
        ('/foo/bar/sub-07_T1w.nii', nib.Nifti1Image),
        ('http://localhost:8999/sub-07_T1w.nii', nib.Nifti1Image),
        ('/foo/bar/sub-07_T1w.mnc', nib.Minc1Image),
        ('http://localhost:8999/sub-07_T1w.mnc', nib.Minc1Image),
    ):
        assert _path2class(url) == exp_class


def test_drop_suffix():
    for inp, suffixes, exp_out in (
        ('foo/bar', ['.nii'], 'foo/bar'),
        ('foo/bar', '.nii', 'foo/bar'),
        ('foo/bar.baz', ['.nii'], 'foo/bar.baz'),
        ('foo/bar.nii', ['.nii'], 'foo/bar'),
        ('foo/bar.nii', '.nii', 'foo/bar'),
        ('foo/bar.nii.gz', ['.nii'], 'foo/bar.nii.gz'),
        ('foo/bar.nii.gz', ['.nii.gz', '.nii'], 'foo/bar'),
    ):
        assert drop_suffix(inp, suffixes) == exp_out
        assert drop_suffix(Path(inp), suffixes) == Path(exp_out)


def test_replace_suffix():
    for inp, suffixes, new_suffix, exp_out in (
        ('foo/bar', ['.nii'], '.json', 'foo/bar.json'),
        ('foo/bar', '.nii', '.json', 'foo/bar.json'),
        ('foo/bar.baz', ['.nii'], '.boo', 'foo/bar.boo'),
        ('foo/bar.nii', ['.nii'], '.boo', 'foo/bar.boo'),
        ('foo/bar.nii', '.nii', '.boo', 'foo/bar.boo'),
        ('foo/bar.nii.gz', ['.nii'], '.boo', 'foo/bar.nii.boo'),
        ('foo/bar.nii.gz', ['.nii.gz', '.nii'], '.boo', 'foo/bar.boo'),
    ):
        assert replace_suffix(inp, suffixes, new_suffix) == exp_out
        assert replace_suffix(Path(inp), suffixes, new_suffix) == Path(exp_out)


def test_json_attrs():
    # Test utilities to load / save JSON attrs
    d = {'foo': 1, 'bar': [2, 3]}
    assert _attrs2json_attrs(d) == d
    assert _json_attrs2attrs(d) == d
    dd = {'foo': 1, 'bar': {'baz': 4}}
    ddj = {'foo': 1, 'bar': ['__json__', '{"baz": 4}']}
    assert _attrs2json_attrs(dd) == ddj
    assert _json_attrs2attrs(ddj) == dd
    arr = rng.integers(0, 10, size=(3, 4)).tolist()
    arr_j = json.dumps(arr)
    dd = {'foo': 1, 'bar': {'baz': [2, 3]}, 'baf': arr}
    ddj = {'foo': 1,
           'bar': ['__json__', '{"baz": [2, 3]}'],
           'baf': ['__json__', arr_j]}
    assert _attrs2json_attrs(dd) == ddj
    assert _json_attrs2attrs(ddj) == dd
    ragged_arr = {'foo': {'bar': [[1], [2, 3]]}}
    raj = {'foo': ['__json__', '{"bar": [[1], [2, 3]]}']}
    assert _attrs2json_attrs(ragged_arr) == raj
    assert _json_attrs2attrs(raj) == ragged_arr


def test_jdumps():
    d = {'foo': 1, 'bar': [2, 3]}
    assert json.loads(_jdumps(d)) == d

    class C:
        pass

    bad_d = {'foo': C()}
    with pytest.raises(TypeError):
        _jdumps(bad_d)


def _check_dims_coords(ximg):
    ndims = len(ximg.dims)
    space_dims = ximg.dims[:3]
    assert space_dims == _NI_SPACE_DIMS
    assert space_dims == tuple(ximg.coords)[:3]
    for dim_no, dim in enumerate(space_dims):
        coord = ximg.coords[dim]
        assert np.all(np.array(coord) == np.arange(ximg.shape[dim_no]))
    if ndims > 3:
        assert ximg.dims[3] == _NI_TIME_DIM


@skip_without_file(JC_EG_FUNC)
def test_nib_loader_jc():
    img = nib.load(JC_EG_FUNC)
    ximg = load_nibabel(JC_EG_FUNC)
    assert ximg.attrs == JC_EG_FUNC_ATTRS
    _check_dims_coords(ximg)
    assert np.all(np.array(ximg) == img.get_fdata())


@skip_without_file(JH_EG_FUNC)
def test_nib_loader_jh():
    img = nib.load(JH_EG_FUNC)
    ximg = load_nibabel(JH_EG_FUNC)
    assert ximg.attrs == {'RepetitionTime': 2.5,
                          'xib-affines':
                          {'scanner': img.affine.tolist()}
                         }
    _check_dims_coords(ximg)


if fetcher.have_file(JC_EG_FUNC):
    img = nib.load(JC_EG_FUNC)
    JC_EG_FUNC_ATTRS = json.loads(JC_EG_FUNC_JSON.read_text())
    JC_EG_FUNC_ATTRS_RAW = {
        'xib-FrequencyEncodingDirection': 'i',
         'PhaseEncodingDirection': 'j',
         'SliceEncodingDirection': 'k',
         'RepetitionTime': 2.0,
         'xib-affines':
         {'scanner': img.affine.tolist()}
    }
    JC_EG_FUNC_ATTRS.update(JC_EG_FUNC_ATTRS_RAW)
else:  # For parametrized tests.
    JC_EG_FUNC_ATTRS = {}
    JC_EG_FUNC_ATTRS_RAW = {}


if fetcher.have_file(JC_EG_ANAT):
    img = nib.load(JC_EG_ANAT)
    JC_EG_ANAT_ATTRS = json.loads(JC_EG_ANAT_JSON.read_text())
    JC_EG_ANAT_ATTRS_RAW = {
        'xib-FrequencyEncodingDirection': 'j',
         'PhaseEncodingDirection': 'i',
         'SliceEncodingDirection': 'k',
         'xib-affines':
         {'scanner': img.affine.tolist()}
    }
    JC_EG_ANAT_ATTRS.update(JC_EG_ANAT_ATTRS_RAW)
else:  # For parametrized tests.
    JC_EG_ANAT_ATTRS = {}
    JC_EG_ANAT_ATTRS_RAW = {}



@skip_without_file(JC_EG_ANAT)
def test_anat_loader():
    img = nib.load(JC_EG_ANAT)
    for loader, in_path in product(
        (load, load_bids, load_nibabel),
        (JC_EG_ANAT, str(JC_EG_ANAT),
         JC_EG_ANAT_JSON, str(JC_EG_ANAT_JSON))):
        ximg = loader(in_path)
        assert ximg.shape == (176, 256, 256)
        assert ximg.dims == _NI_SPACE_DIMS
        assert ximg.name == JC_EG_ANAT.name.split('.')[0]
        assert ximg.attrs == JC_EG_ANAT_ATTRS
        _check_dims_coords(ximg)
        assert np.all(np.array(ximg) == img.get_fdata())


@skip_without_file(JC_EG_ANAT)
@skip_without_file(JC_EG_ANAT_JSON)
def test_anat_loader_http(fserver):
    nb_img = nib.load(JC_EG_ANAT)
    # Read nibabel from HTTP
    # Original gz
    name_gz = JC_EG_ANAT.name
    # Uncompressed, no gz
    name_no_gz = JC_EG_ANAT.with_suffix('').name
    out_path = fserver.server_path / name_no_gz
    nib.save(nb_img, out_path)
    for name in (name_gz, name_no_gz):
        out_url = fserver.make_url(name)
        ximg = load(out_url)
        # Check we can read the data
        ximg.compute()
        # Check parameters
        assert ximg.shape == (176, 256, 256)
        assert ximg.name == JC_EG_ANAT.name.split('.')[0]
        assert ximg.attrs == JC_EG_ANAT_ATTRS
        _check_dims_coords(ximg)
        assert np.all(np.array(ximg) == nb_img.get_fdata())
    # Refuse to load pair files.
    pair_path = fserver.server_path / 'pair.img'
    nib.save(nb_img, pair_path)
    json_path = fserver.server_path / 'pair.json'
    json_path.write_text(JC_EG_ANAT_JSON.read_text())
    for name in (pair_path.name, json_path.name):
        out_url = fserver.make_url(name)
        with pytest.raises(XibFileError):
            load(out_url)


@skip_without_file(JC_EG_ANAT)
def test_anat_loader_http_params(fserver, tmp_path):
    # Test params get passed through in kwargs.
    nb_img = nib.load(JC_EG_ANAT)
    out_url = 'simplecache::' + fserver.make_url(JC_EG_ANAT.name)
    out_cache = tmp_path / 'files'
    assert not out_cache.is_dir()
    ximg = load(out_url,
                simplecache={'cache_storage': str(out_cache)})
    assert np.all(np.array(ximg) == nb_img.get_fdata())
    assert out_cache.is_dir()
    assert len(list(out_cache.glob('*'))) == 2  # JSON and Nifti


@skip_without_file(JC_EG_ANAT)
def test_round_trip(tmp_path):
    ximg = load(JC_EG_ANAT)
    assert ximg.shape == (176, 256, 256)
    _check_dims_coords(ximg)
    out_path = tmp_path / 'out.ximg'
    save(ximg, out_path)
    back = load(out_path)
    assert back.shape == (176, 256, 256)
    assert back.attrs == JC_EG_ANAT_ATTRS
    _check_dims_coords(back)
    # And again
    save(ximg, out_path)
    back = load(out_path)
    assert back.attrs == JC_EG_ANAT_ATTRS
    _check_dims_coords(back)
    # With url
    back = load(f'file:///{out_path}')
    assert back.attrs == JC_EG_ANAT_ATTRS
    _check_dims_coords(back)


@skip_without_file(JC_EG_ANAT)
def test_rt_header(tmp_path):
    # Modifying header modifies ximg and out
    in_path = tmp_path / 'in.nii'
    out_path = tmp_path / 'out.nii'
    nimg = nib.load(JC_EG_ANAT)
    old_affine = nimg.affine.copy()
    new_affine = np.diag([2.1, 3.2, 4.1, 1])
    new_affine[:3, 3] = [11, 12, 13]
    nib.save(nimg, in_path)
    ximg = load(in_path)
    assert arr_dict_allclose(ximg.xi.get_affines(), {'scanner': old_affine})
    save(ximg, out_path)
    ximg = load(out_path)
    assert arr_dict_allclose(ximg.xi.get_affines(), {'scanner': old_affine})
    nimg.set_sform(new_affine, 'scanner')
    nib.save(nimg, in_path)
    ximg = load(in_path)
    assert arr_dict_allclose(ximg.xi.get_affines(), {'scanner': new_affine})
    save(ximg, out_path)
    ximg = load(out_path)
    assert arr_dict_allclose(ximg.xi.get_affines(), {'scanner': new_affine})
    nimg.set_sform(new_affine, 'aligned')
    nib.save(nimg, in_path)
    ximg = load(in_path)
    assert arr_dict_allclose(ximg.xi.get_affines(),
                             {'aligned': new_affine, 'scanner': old_affine})
    save(ximg, out_path)
    ximg = load(out_path)
    assert arr_dict_allclose(ximg.xi.get_affines(),
                             {'aligned': new_affine, 'scanner': old_affine})
    nimg.set_sform(new_affine, 'template')
    nib.save(nimg, in_path)
    ximg = load(in_path)
    assert arr_dict_allclose(ximg.xi.get_affines(),
                             {'template': new_affine, 'scanner': old_affine})
    save(ximg, out_path)
    ximg = load(out_path)
    assert arr_dict_allclose(ximg.xi.get_affines(),
                             {'template': new_affine, 'scanner': old_affine})
    nimg.set_qform(old_affine, 'mni')
    nimg.set_sform(new_affine, 'aligned')
    nib.save(nimg, in_path)
    ximg = load(in_path)
    assert arr_dict_allclose(ximg.xi.get_affines(),
                             {'mni': old_affine, 'aligned': new_affine})
    save(ximg, out_path)
    ximg = load(out_path)
    assert arr_dict_allclose(ximg.xi.get_affines(),
                             {'mni': old_affine, 'aligned': new_affine})


@h5netcdf_test
@skip_without_file(JC_EG_ANAT)
def test_round_trip_netcdf(tmp_path):
    ximg = load(JC_EG_ANAT)
    out_path = tmp_path / 'out.nc'
    save(ximg, out_path)
    back = load(out_path)
    assert back.shape == (176, 256, 256)
    assert back.attrs == JC_EG_ANAT_ATTRS
    back = load(f'file:///{out_path}')
    assert back.attrs == JC_EG_ANAT_ATTRS
    _check_dims_coords(back)


@skip_without_file(JC_EG_ANAT)
@skip_without_file(JC_EG_FUNC)
@pytest.mark.parametrize("img_path", [JC_EG_ANAT, JC_EG_FUNC])
def test_affines(img_path):
    ximg = load(img_path)
    nib_img = nib.load(img_path)
    affines = ximg.xi.get_affines()
    assert list(affines) == ['scanner']
    assert np.all(affines['scanner'] == nib_img.affine)
    back = ximg.xi.with_updated_affines()
    assert np.all(back.xi.get_affines()['scanner'] == nib_img.affine)
    xT = ximg.T
    sp_dims = _NI_SPACE_DIMS
    assert xT.dims == ximg.dims[::-1]
    transposed = xT.xi.with_updated_affines()
    assert np.all(transposed.xi.get_affines()['scanner'] == nib_img.affine)
    for i, (name, slice_no) in enumerate(zip(sp_dims, (42, 32, 10))):
        ximg_plane = ximg.sel(**{name: slice_no})
        assert ximg_plane.dims == tuple(d for d in ximg.dims if d != name)
        assert tuple(ximg_plane.coords) == ximg.dims
        adj_img = ximg_plane.xi.with_updated_affines()
        new_origin = np.array([0, 0, 0, 1])
        new_origin[i] = slice_no
        new_affine = nib_img.affine.copy()
        new_affine[:, 3] = nib_img.affine @ new_origin
        assert np.all(adj_img.xi.get_affines()['scanner'] == new_affine)
        # Check Nibabel slicer gives the same result.
        slicers = [slice(None) for d in range(len(ximg.dims))]
        slicers[i] = slice(slice_no, slice_no + 1)
        assert np.all(nib_img.slicer[tuple(slicers)].affine == new_affine)
    for i, (name, spacing) in enumerate(zip(sp_dims, (2, 3, 4))):
        slicers = [slice(None) for d in range(len(ximg.dims))]
        slicers[i] = slice(None, None, spacing)
        ximg_sliced = ximg[tuple(slicers)]
        assert ximg_sliced.dims == ximg.dims
        assert tuple(ximg_sliced.coords) == ximg.dims
        adj_img = ximg_sliced.xi.with_updated_affines()
        new_affine = nib_img.affine.copy()
        scalers = np.ones(3)
        scalers[i] = spacing
        new_affine[:3, :3] = nib_img.affine[:3, :3] @ np.diag(scalers)
        assert np.all(adj_img.xi.get_affines()['scanner'] == new_affine)
        # Check Nibabel slicer gives the same result.
        assert np.all(nib_img.slicer[tuple(slicers)].affine == new_affine)
    # Some more complex slicings, benchmark against nibabel
    for slicers in permutations([slice(10, 20, 2),
                                 slice(30, 15, -1),
                                 slice(5, 16, 3)]):
        sliced_ximg = ximg[tuple(slicers)].xi.with_updated_affines()
        sliced_nib_img = nib_img.slicer[tuple(slicers)]
        assert np.all(sliced_ximg.xi.get_affines()['scanner'] ==
                    sliced_nib_img.affine)


def test_tornado(fserver):
    # Test static file server for URL reads
    fserver.write_text_to('text_file', 'some text')
    fserver.write_bytes_to('binary_file', b'binary')
    response = fserver.get('text_file')
    assert response.status_code == 200
    assert response.text == 'some text'
    assert fserver.read_text('text_file') == 'some text'
    assert fserver.read_bytes('text_file') == b'some text'
    assert fserver.read_bytes('binary_file') == b'binary'


@h5netcdf_test
@skip_without_file(JC_EG_ANAT)
def test_round_trip_netcdf_url(fserver):
    ximg = load(JC_EG_ANAT)
    save(ximg, fserver.server_path / 'out.nc')
    out_url = fserver.make_url('out.nc')
    back = load(out_url)
    assert back.shape == (176, 256, 256)
    assert back.attrs == JC_EG_ANAT_ATTRS
    _check_dims_coords(back)


@skip_without_file(JC_EG_ANAT)
def test_matching_img_error(tmp_path):
    out_json = tmp_path / JC_EG_ANAT_JSON.name
    with pytest.raises(XibFileError, match='does not appear to exist'):
        load(out_json)
    shutil.copy2(JC_EG_ANAT_JSON, tmp_path)
    with pytest.raises(XibFileError, match='No valid file matching'):
        load(out_json)
    out_img = tmp_path / JC_EG_ANAT.name
    shutil.copy2(JC_EG_ANAT, tmp_path)
    back = load(out_img)
    assert back.shape == (176, 256, 256)
    assert back.attrs == JC_EG_ANAT_ATTRS
    _check_dims_coords(back)
    os.unlink(out_img)
    with pytest.raises(XibFileError, match='does not appear to exist'):
        load(out_img)
    shutil.copy2(JC_EG_ANAT, tmp_path)
    os.unlink(out_json)
    back = load(out_img)
    _check_dims_coords(back)
    assert back.attrs == JC_EG_ANAT_ATTRS_RAW
    back = load_bids(out_img, require_json=False)
    assert back.attrs == JC_EG_ANAT_ATTRS_RAW
    _check_dims_coords(back)
    with pytest.raises(XibFileError, match='`require_json` is True'):
        load_bids(out_img, require_json=True)


def test_ni_sort_expand_dims():
    assert _ni_sort_expand_dims([]) == ([],
                                        ['i', 'j', 'k'],
                                        [0, 1, 2])
    assert _ni_sort_expand_dims(['time']) == (['time'],
                                              ['i', 'j', 'k'],
                                              [0, 1, 2])
    assert (_ni_sort_expand_dims(['j']) ==
            (['j'],
             ['i', 'k'],
             [0, 2]))
    assert (_ni_sort_expand_dims(['time', 'j']) ==
            (['j', 'time'],
             ['i', 'k'],
             [0, 2]))
    assert (_ni_sort_expand_dims(['j', 'i']) ==
            (['i', 'j'],
             ['k'],
             [2]))
    assert (_ni_sort_expand_dims(['time', 'j', 'k']) ==
            (['j', 'k', 'time'],
             ['i'],
             [0]))


@skip_without_file(JC_EG_ANAT)
@skip_without_file(JC_EG_FUNC)
@pytest.mark.parametrize("img_path, attrs_raw",
                         ((JC_EG_ANAT, JC_EG_ANAT_ATTRS_RAW),
                          (JC_EG_FUNC, JC_EG_FUNC_ATTRS_RAW)))
def test_to_nifti(img_path, attrs_raw):
    orig_img = nib.load(img_path)
    orig_data = orig_img.get_fdata()
    ximg = load(img_path)
    # Check data is the same for basic load.
    assert np.all(ximg == orig_data)
    # Basic conversion.
    img, attrs = to_nifti(ximg)
    assert np.all(img.get_fdata() == orig_data)
    assert arr_dict_allclose(hdr2attrs(img.header), attrs_raw)
    img, attrs = to_nifti(ximg.T)
    assert np.all(img.get_fdata() == orig_data)
    assert arr_dict_allclose(hdr2attrs(img.header), attrs_raw)
    img, attrs = to_nifti(ximg.T.sel(k=32))  # Drop k axis
    assert np.all(img.get_fdata() == orig_data[:, :, 32:33])
    # This changes the origin of the affine.
    new_affine = orig_img.slicer[:, :, 32:33].affine
    exp_attrs_32 = deepcopy(attrs_raw)
    exp_attrs_32['xib-affines']['scanner'] = new_affine
    assert arr_dict_allclose(hdr2attrs(img.header), exp_attrs_32)


@skip_without_file(JC_EG_ANAT)
@skip_without_file(JC_EG_FUNC)
@pytest.mark.parametrize("img_path, attrs",
                         ((JC_EG_ANAT, JC_EG_ANAT_ATTRS),
                          (JC_EG_FUNC, JC_EG_FUNC_ATTRS)))
def test_to_bids(img_path, attrs, tmp_path):
    nib_img = nib.load(img_path)
    fdata = nib_img.get_fdata()
    ximg = load(img_path)
    out_fname = tmp_path / 'out.json'
    save(ximg, out_fname)
    back_nib = nib.load(tmp_path / 'out.nii.gz')
    assert np.allclose(back_nib.get_fdata(), fdata)
    with open(out_fname, 'rt') as fobj:
        back_attrs = json.load(fobj)
    assert arr_dict_allclose(back_attrs, attrs)
    assert arr_dict_allclose(load(out_fname).attrs, ximg.attrs)
    out_fname = tmp_path / 'out2.nii'
    save(ximg, out_fname)
    back_nib = nib.load(out_fname)
    assert np.allclose(back_nib.get_fdata(), fdata)
    with open(tmp_path / 'out2.json', 'rt') as fobj:
        back_attrs = json.load(fobj)
    assert arr_dict_allclose(back_attrs, attrs)
    assert arr_dict_allclose(load(out_fname).attrs, ximg.attrs)


def test_loadsave_errors(tmp_path):
    ximg = from_array(np.arange(24).reshape((2, 3, 4)))
    save(ximg, tmp_path / 'ok.nii')
    # Nibabel, wrong format.
    with pytest.raises(nib.filebasedimages.ImageFileError):
        save(ximg, tmp_path / 'bad1.foo')
    # Nibabel, forced wrong format.
    with pytest.raises(XibFormatError):
        save(ximg, tmp_path / 'bad1.nii', format='foo')
    # Nibabel, forced wrong format for load.
    with pytest.raises(XibFormatError):
        save(ximg, tmp_path / 'ok.nii', format='foo')
