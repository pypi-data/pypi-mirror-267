import pytest

from toptica.lasersdk.decop import DecopError
from toptica.lasersdk.decop import DecopValueError

from toptica.lasersdk.decop import decode_value_inferred

from toptica.lasersdk.decop import _match_bool
from toptica.lasersdk.decop import _match_int
from toptica.lasersdk.decop import _match_float
from toptica.lasersdk.decop import _match_string
from toptica.lasersdk.decop import _match_bytes
from toptica.lasersdk.decop import _match_tuple


@pytest.mark.parametrize("test, expected", [
    ('#t', True), ('#T', True), ('#f', False), ('#F', False)
])
def test_decode_value_inferred_bool(test, expected):
    assert decode_value_inferred(test) == expected


@pytest.mark.parametrize("test, expected", [
    ('-1', -1), ('-0', 0), ('0', 0), ('+0', 0), ('1', 1), ('+1', 1),
    ('-2147483648', -2147483648), ('2147483647', 2147483647)
])
def test_decode_value_inferred_int(test, expected):
    assert decode_value_inferred(test) == expected


@pytest.mark.parametrize("test, expected", [
    ('-1.0', -1.0), ('-0.0', 0), ('0.0', 0.0), ('+0.0', 0.0), ('1.0', 1.0), ('+1.0', 1.0),
    ('-1.0e-12', -1.0e-12), ('-1.0e+12', -1.0e+12),
    ('+1.0e-12', +1.0e-12), ('+1.0e-12', +1.0e-12),
])
def test_decode_value_inferred_float(test, expected):
    assert decode_value_inferred(test) == expected


@pytest.mark.parametrize("test, expected", [
    ('""', ''), ('" "', ' '), ('"x"', 'x')
])
def test_decode_value_inferred_str(test, expected):
    assert decode_value_inferred(test) == expected


@pytest.mark.parametrize("test, expected", [
    ('&"YWQgYXN0cmEgcGVyIGFzcGVyYQ=="', b'ad astra per aspera')
])
def test_decode_value_inferred_bytes(test, expected):
    assert decode_value_inferred(test) == expected


@pytest.mark.parametrize("test, expected", [
    ('()', ())
])
def test_decode_value_inferred_tuple(test, expected):
    assert decode_value_inferred(test) == expected


@pytest.mark.parametrize("test", [
    '', '.', '(', '#', '(()'
])
def test_decode_value_inferred_fail(test):
    with pytest.raises(DecopValueError) as exc:
        decode_value_inferred(test)
    assert str(exc.value) == "Failed to infer type for {!r}".format(test)


def test_decode_value_inferred_error():
    with pytest.raises(DecopError) as exc:
        decode_value_inferred('Error: -303 there is no spoon')
    assert str(exc.value) == 'Error: -303 there is no spoon'


# --- decop._match_bool -------------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("test, expected", [
    ('#t', True), ('#T', True), ('#f', False), ('#F', False)
])
def test_match_bool(test, expected):
    assert _match_bool(test) == ('', expected)


@pytest.mark.parametrize("delim", [
    '(', ')', '\t', '\v', '\f', '\r', '\n', ' '
])
@pytest.mark.parametrize("value, expected", [
    ('#t', True), ('#T', True), ('#f', False), ('#F', False)
])
def test_match_bool_delim(delim, value, expected):
    assert _match_bool(value + delim) == (delim, expected)


@pytest.mark.parametrize("test", [
    '', '#', '##', '#x', '#5'
])
def test_match_bool_fail(test):
    assert _match_bool(test) == (test, None)


def test_match_bool_preserve_input():
    test = '#t'
    assert _match_bool(test) == ('', True)
    assert test == '#t'


# --- decop._match_int --------------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("test", [
    '0', '1', '+5', '-7', '+123', '-456', '123456', '0001', '-0001', '+0001'
])
def test_match_int(test):
    assert _match_int(test) == ('', int(test))


@pytest.mark.parametrize("delim", [
    '(', ')', '\t', '\v', '\f', '\r', '\n', ' '
])
@pytest.mark.parametrize("value", [
    '0', '1', '+5', '-7', '+123', '-456', '123456', '0001', '-0001', '+0001'
])
def test_match_int_delim(delim, value):
    assert _match_int(value + delim) == (delim, int(value))


@pytest.mark.parametrize("test", [
    '', '.', '1.0', '1e10', '+', '-'
])
def test_match_int_fail(test):
    assert _match_int(test) == (test, None)


def test_match_int_preserve_input():
    test = '123'
    assert _match_int(test) == ('', 123)
    assert test == '123'


# --- decop._match_float ------------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("test", [
    '0.0', '1.2', '+1.2', '-1.2', '1.', '+1.', '-1.', '.2', '+.2', '-.2', '0001.2000'
])
def test_match_float(test):
    assert _match_float(test) == ('', float(test))


@pytest.mark.parametrize("delim", [
    '(', ')', '\t', '\v', '\f', '\r', '\n', ' '
])
@pytest.mark.parametrize("value", [
    '1.2', '1.', '.2'
])
def test_match_float_delim(delim, value):
    assert _match_float(value + delim) == (delim, float(value))


@pytest.mark.parametrize("test", [
    '', '.', '1..0', '1.2.3', 'xyz', 'x.y', '1+.0', '1.0-', '12', '++1.0'
])
def test_match_float_fail(test):
    assert _match_float(test) == (test, None)


@pytest.mark.parametrize("test", [
    '0e0', '1e+2', '1e-2', '001e02', '001e+02', '001e-02'
])
def test_match_float_exp(test):
    assert _match_float(test) == ('', float(test))


@pytest.mark.parametrize("test", [
    '1e', '1e+', '1e-', '1e-', '1e.', '1e++1', '1e--1', '1ee2'
])
def test_match_float_exp_fail(test):
    assert _match_float(test) == (test, None)


@pytest.mark.parametrize("delim", [
    '(', ')', '\t', '\v', '\f', '\r', '\n', ' '
])
@pytest.mark.parametrize("value", [
    '1.2e5', '1.e7', '.2e+3'
])
def test_match_float_exp_delim(delim, value):
    assert _match_float(value + delim) == (delim, float(value))


def test_match_float_preserve_input():
    test = '1.2'
    assert _match_float(test) == ('', 1.2)
    assert test == '1.2'


# --- decop._match_string -----------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("test, expected", [
    ('""', ''), ('" "', ' '), ('"xyz"', 'xyz'), (r'"\""', r'\"'), (r'"\\"', r'\\')
])
def test_match_string(test, expected):
    assert _match_string(test) == ('', expected)


@pytest.mark.parametrize("delim", [
    '(', ')', '\t', '\v', '\f', '\r', '\n', ' '
])
@pytest.mark.parametrize("value, expected", [
    ('""', ''), ('" "', ' '), ('"xyz"', 'xyz'), (r'"\""', r'\"'), (r'"\\"', r'\\')
])
def test_match_string_delim(delim, value, expected):
    assert _match_string(value + delim) == (delim, expected)


@pytest.mark.parametrize("test", [
    '', '"', 'x', '"xyz'
])
def test_match_string_fail(test):
    assert _match_string(test) == (test, None)


def test_match_string_preserve_input():
    test = '"xyz"'
    assert _match_string(test) == ('', 'xyz')
    assert test == '"xyz"'


# --- decop._match_binary -----------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("test, expected", [
    ('&', b''), ('&Zg==', b'f'), ('&Zm8=', b'fo'), ('&Zm9v', b'foo'), ('&Zm9vYg==', b'foob'),
    ('&Zm9vYmE=', b'fooba'), ('&Zm9vYmFy', b'foobar')
])
def test_match_bytes(test, expected):
    assert _match_bytes(test) == ('', expected)


@pytest.mark.parametrize("delim", [
    '(', ')', '\t', '\v', '\f', '\r', '\n', ' '
])
@pytest.mark.parametrize("value, expected", [
    ('&', b''), ('&Zg==', b'f'), ('&Zm8=', b'fo'), ('&Zm9v', b'foo'), ('&Zm9vYg==', b'foob'),
    ('&Zm9vYmE=', b'fooba'), ('&Zm9vYmFy', b'foobar')
])
def test_match_bytes_delim(delim, value, expected):
    assert _match_bytes(value + delim) == (delim, expected)


@pytest.mark.parametrize("test", [
    '', '""', '"Zg=="', '&._', '&Zm9vYmFy-'
])
def test_match_bytes_fail(test):
    assert _match_bytes(test) == (test, None)


def test_match_bytes_preserve_input():
    test = '&Zm9vYmFy'
    assert _match_bytes(test) == ('', b'foobar')
    assert test == '&Zm9vYmFy'


# --- decop._match_tuple -------------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("test, expected", [
    ('()', ()), ('(1)', (1,)), ('(1.2)', (1.2,)), ('(#t)', (True,)), ('("xyz")', ('xyz',)), ('(#t 0)', (True, 0))
])
def test_match_tuple_0(test, expected):
    assert _match_tuple(test) == ('', expected)


@pytest.mark.parametrize("test, expected", [
    ('(.3 12)', (0.3, 12)), ('("xyz" &Zg== -5)', ('xyz', b'f', -5))
])
def test_match_tuple_1(test, expected):
    assert _match_tuple(test) == ('', expected)


@pytest.mark.parametrize("test, expected", [
    ('(1 (2 3))', (1, (2, 3))), ('((1 2) 3)', ((1, 2), 3)), ('((1 2) (3 4))', ((1, 2), (3, 4))),
    ('((1 (2 3)) ((3 4) 5))', ((1, (2, 3)), ((3, 4), 5)))
])
def test_match_tuple_within_tuple(test, expected):
    assert _match_tuple(test) == ('', expected)


@pytest.mark.parametrize("test", [
    '', '(', ')', '(1 (', '((', '(_', '(()', '[]', '(-)'
])
def test_match_tuple_fail(test):
    assert _match_tuple(test) == (test, None)


def test_match_tuple_preserve_input():
    test = '(1 2 ((3 4) 5))'
    assert _match_tuple(test) == ('', (1, 2, ((3, 4), 5)))
    assert test == '(1 2 ((3 4) 5))'
