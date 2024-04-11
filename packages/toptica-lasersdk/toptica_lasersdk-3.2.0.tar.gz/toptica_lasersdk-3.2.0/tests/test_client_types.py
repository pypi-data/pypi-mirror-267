import pytest

from mock import MagicMock

from toptica.lasersdk.client import Client
from toptica.lasersdk.client import Subscription

from toptica.lasersdk.client import DecopBoolean
from toptica.lasersdk.client import DecopInteger
from toptica.lasersdk.client import DecopReal
from toptica.lasersdk.client import DecopString
from toptica.lasersdk.client import DecopBinary

from toptica.lasersdk.client import MutableDecopBoolean
from toptica.lasersdk.client import MutableDecopInteger
from toptica.lasersdk.client import MutableDecopReal
from toptica.lasersdk.client import MutableDecopString
from toptica.lasersdk.client import MutableDecopBinary

from toptica.lasersdk.client import SettableDecopBoolean
from toptica.lasersdk.client import SettableDecopInteger
from toptica.lasersdk.client import SettableDecopReal
from toptica.lasersdk.client import SettableDecopString
from toptica.lasersdk.client import SettableDecopBinary


@pytest.fixture
def client():
    return MagicMock(spec=Client)


@pytest.fixture
def callback():
    return lambda: None


@pytest.fixture
def subscription(client, callback):
    return Subscription(client, 'param-name', callback)


@pytest.mark.parametrize(
    "client_type, return_value", [(DecopBoolean, True),   (MutableDecopBoolean, True),   (SettableDecopBoolean, True),
                                  (DecopInteger, 7),      (MutableDecopInteger, 7),      (SettableDecopInteger, 7),
                                  (DecopReal,    2.7182), (MutableDecopReal,    2.7182), (SettableDecopReal,    2.7182),
                                  (DecopString,  'abc'),  (MutableDecopString,  'abc'),  (SettableDecopString,  'abc'),
                                  (DecopBinary,  b'xyz'), (MutableDecopBinary,  b'xyz'), (SettableDecopBinary,  b'xyz')]
)
def test_get_calls_client_get(client_type, return_value):
    """Test if querying a parameter calls the get-method of the client."""
    client = MagicMock(spec=Client, **{'get.return_value': return_value})

    param = client_type(client, 'param-name')
    result = param.get()

    assert result == return_value
    client.get.assert_called_once_with('param-name', type(return_value))


@pytest.mark.parametrize(
    "client_type, return_value", [(SettableDecopBoolean, True),
                                  (SettableDecopInteger, 7),
                                  (SettableDecopReal,    2.7182),
                                  (SettableDecopString,  'abc'),
                                  (SettableDecopBinary,  b'xyz')]
)
def test_get_set_value_calls_client_get_set_value(client_type, return_value):
    """Test if querying a parameter calls the get-method of the client."""
    client = MagicMock(spec=Client, **{'get_set_value.return_value': return_value})

    param = client_type(client, 'param-name')
    result = param.get_set_value()

    assert result == return_value
    client.get_set_value.assert_called_once_with('param-name', type(return_value))


@pytest.mark.parametrize(
    "client_type, value", [(MutableDecopBoolean, True),              (SettableDecopBoolean, True),
                           (MutableDecopInteger, 7),                 (SettableDecopInteger, 7),
                           (MutableDecopReal,    2),                 (SettableDecopReal,    2),
                           (MutableDecopReal,    2.7182),            (SettableDecopReal,    2.7182),
                           (MutableDecopString,  'abc'),             (SettableDecopString,  'abc'),
                           (MutableDecopBinary,  b'xyz'),            (SettableDecopBinary,  b'xyz'),
                           (MutableDecopBinary,  bytearray(b'uvw')), (SettableDecopBinary,  bytearray(b'uvw'))]
)
def test_set_calls_client_set(client_type, value):
    """Test if setting a parameter calls the set-method of the client."""
    client = MagicMock(spec=Client, **{'set.return_value': 7})

    param = client_type(client, 'param-name')
    result = param.set(value)

    assert result == 7
    client.set.assert_called_once_with('param-name', value)


@pytest.mark.parametrize(
    "client_type, value", [(MutableDecopBoolean, 7),      (SettableDecopBoolean, 7),
                           (MutableDecopInteger, 'abc'),  (SettableDecopInteger, 'abc'),
                           (MutableDecopReal,    b'xyz'), (SettableDecopReal,    b'xyz'),
                           (MutableDecopString,  2.7182), (SettableDecopString,  2.7182),
                           (MutableDecopBinary,  True),   (SettableDecopBinary,  True)]
)
def test_set_with_invalid_type(client, client_type, value):
    """Test if setting a parameter value with an invalid type raises an AssertionError."""
    param = client_type(client, 'param-name')

    with pytest.raises(AssertionError):
        param.set(value)

    client.set.assert_not_called()


@pytest.mark.parametrize(
    "client_type, py_type", [(DecopBoolean, bool),  (MutableDecopBoolean, bool),  (SettableDecopBoolean, bool),
                             (DecopInteger, int),   (MutableDecopInteger, int),   (SettableDecopInteger, int),
                             (DecopReal,    float), (MutableDecopReal,    float), (SettableDecopReal,    float),
                             (DecopString,  str),   (MutableDecopString,  str),   (SettableDecopString,  str),
                             (DecopBinary,  bytes), (MutableDecopBinary,  bytes), (SettableDecopBinary,  bytes)]
)
def test_subscribe_calls_client_subscribe(callback, subscription, client_type, py_type):
    """Test if subscribing to a parameter calls the subscribe-method of the client."""
    client = MagicMock(spec=Client, **{'subscribe.return_value': subscription})

    param = client_type(client, 'param-name')
    result = param.subscribe(callback)

    assert result == subscription
    client.subscribe.assert_called_once_with('param-name', callback, py_type)


@pytest.mark.parametrize(
    "client_type", [DecopBoolean, MutableDecopBoolean, SettableDecopBoolean,
                    DecopInteger, MutableDecopInteger, SettableDecopInteger,
                    DecopReal,    MutableDecopReal,    SettableDecopReal,
                    DecopString,  MutableDecopString,  SettableDecopString,
                    DecopBinary,  MutableDecopBinary,  SettableDecopBinary]
)
def test_name_returns_init_value(client, client_type):
    """Test if the name-property of a parameter returns the provided value."""
    param = client_type(client, 'param-name')
    assert param.name == 'param-name'
