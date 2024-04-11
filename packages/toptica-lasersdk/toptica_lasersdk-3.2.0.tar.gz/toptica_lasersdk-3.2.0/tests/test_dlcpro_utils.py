import pytest

from toptica.lasersdk.utils.dlcpro import *


def test_float_array_block():
    assert extract_float_arrays('x', b'x4\0\x00\x00\x80\x3f')['x'][0] == 1.0


def test_lock_point_block():
    data = b'c9\0\x00\x00\x80\x3f\x00\x00\x80\x3f\0'
    assert extract_lock_points('c', data)['c'] == {'x': [1.0], 'y': [1.0], 't': '\0'}


def test_zero_length_float_array_blocks():
    blockids = 'xyYaAbB'
    assert set(extract_float_arrays(blockids, b'x0\0y0\0Y0\0a0\0A0\0b0\0B0\0').keys()) == set(blockids)


def test_zero_length_lockpoint_blocks():
    blockids = 'clt'
    assert set(extract_lock_points(blockids, b'c0\0l0\0t0\0').keys()) == set(blockids)


@pytest.mark.parametrize('testdata', [b'x', b'x\0', b'x_0\0', b'x1\0', b'x1\0__'])
def test_invalid_float_arrays_data(testdata):
    with pytest.raises(DataFormatError):
        extract_float_arrays('x', testdata)


@pytest.mark.parametrize('testdata', [b'c', b'c\0', b'c_0\0', b'c1\0', b'c1\0__'])
def test_invalid_lock_points_data(testdata):
    with pytest.raises(DataFormatError):
        extract_lock_points('c', testdata)


@pytest.mark.parametrize('testdata', [b's', b's\0', b's_0\0', b's1\0'])
def test_invalid_lock_state_data(testdata):
    with pytest.raises(DataFormatError):
        extract_lock_state(testdata)
