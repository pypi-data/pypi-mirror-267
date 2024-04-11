import pytest

from datetime import datetime

from toptica.lasersdk.decop import DecopError
from toptica.lasersdk.decop import DecopValueError
from toptica.lasersdk.decop import ParamMode
from toptica.lasersdk.decop import StreamType
from toptica.lasersdk.decop import UserLevel

from toptica.lasersdk.decop import access_mode
from toptica.lasersdk.decop import user_level
from toptica.lasersdk.decop import decode_value
from toptica.lasersdk.decop import encode_value
from toptica.lasersdk.decop import stream_type
from toptica.lasersdk.decop import parse_monitoring_line


# --- decop.parse_monitoring_line ---------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize('ending', ['\r\n', '\n'])
def test_parse_monitoring_line(ending):

    line = "(2017-09-07T14:47:45.887Z 'enabled #f)" + ending

    timestamp, name, value = parse_monitoring_line(line)

    assert timestamp == datetime(2017, 9, 7, 14, 47, 45, 887000)
    assert name == 'enabled'
    assert isinstance(value, str)
    assert value == '#f'


@pytest.mark.parametrize('ending', ['\r\n', '\n'])
def test_parse_monitoring_line_error(ending):

    line = "(Error: -1 (2017-09-07T14:47:45.887Z 'laser1:enabled) something happened)" + ending

    timestamp, name, exc = parse_monitoring_line(line)

    assert timestamp == datetime(2017, 9, 7, 14, 47, 45, 887000)
    assert name == 'laser1:enabled'
    assert isinstance(exc, DecopError)
    assert str(exc) == 'Error: -1 something happened'


# --- decop.user_level ------------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize(
    "test, expected",
    [('internal',    UserLevel.INTERNAL),    ('INTERNAL',    UserLevel.INTERNAL),
     ('service',     UserLevel.SERVICE),     ('SERVICE',     UserLevel.SERVICE),
     ('maintenance', UserLevel.MAINTENANCE), ('MAINTENANCE', UserLevel.MAINTENANCE),
     ('readonly',    UserLevel.READONLY),    ('READONLY',    UserLevel.READONLY),
     ('foo', None), ('', None), (None, None)])
def test_user_level(test, expected):
    assert user_level(test) == expected


# --- decop.access_mode ------------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize(
    "test, expected",
    [('readonly',  ParamMode.READONLY),  ('readonly',  ParamMode.READONLY),
     ('writeonly', ParamMode.WRITEONLY), ('writeonly', ParamMode.WRITEONLY),
     ('readwrite', ParamMode.READWRITE), ('readwrite', ParamMode.READWRITE),
     ('readset',   ParamMode.READSET),   ('readset',   ParamMode.READSET),
     ('foo', None), ('', None), (None, None)])
def test_access_mode(test, expected):
    assert access_mode(test) == expected


# --- decop.stream_type -------------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize(
    "test, expected",
    [('base64', StreamType.BASE64), ('BASE64', StreamType.BASE64),
     ('text',   StreamType.TEXT),   ('TEXT',   StreamType.TEXT),
     ('foo', None), ('', None), (None, None)])
def test_stream_type(test, expected):
    assert stream_type(test) == expected


# --- decop.encode_value ------------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("test, expected", [
    (True, '#t'), (False, '#f'), (1024, '1024'), (2.71828, '2.71828'),
    ('ars longa, vita brevis', '"ars longa, vita brevis"'), (b'ad astra per aspera', '"YWQgYXN0cmEgcGVyIGFzcGVyYQ=="')])
def test_encode_value(test, expected):
    assert encode_value(test) == expected


@pytest.mark.parametrize("test", [None, datetime, [], {}, ()])
def test_encode_value_error(test):
    with pytest.raises(DecopError):
        encode_value(test)


# --- decop.decode_value ------------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("test, expected", [
    ('#t', True), ('#T', True), ('#f', False), ('#F', False), ('256', 256), ('3.14159', 3.14159),
    ('"ars longa, vita brevis"', 'ars longa, vita brevis'),
    ('"YWQgYXN0cmEgcGVyIGFzcGVyYQ=="', b'ad astra per aspera'),
    ('&YWQgYXN0cmEgcGVyIGFzcGVyYQ==', b'ad astra per aspera')])
def test_decode_value(test, expected):
    assert decode_value(test, type(expected)) == expected


def test_decode_value_error():
    with pytest.raises(DecopError) as exc:
        decode_value('Error: -303 there is no spoon', int)
    assert str(exc.value) == 'Error: -303 there is no spoon'


def test_decode_value_unknown_type_error():
    with pytest.raises(DecopError):
        decode_value('xyz', complex)


@pytest.mark.parametrize("test", [('1.2', int), ('xyz', float), ('#k', bool), ('"\'', str), ("'\"", str), ("''", str)])
def test_decode_value_type_error(test):
    with pytest.raises(DecopValueError):
        decode_value(*test)
