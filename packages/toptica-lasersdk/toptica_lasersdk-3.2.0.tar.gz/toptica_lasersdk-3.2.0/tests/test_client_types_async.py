import pytest

from mock import AsyncMock

from toptica.lasersdk.asyncio.client import Client
from toptica.lasersdk.asyncio.client import Subscription

from toptica.lasersdk.asyncio.client import DecopBoolean
from toptica.lasersdk.asyncio.client import DecopInteger
from toptica.lasersdk.asyncio.client import DecopReal
from toptica.lasersdk.asyncio.client import DecopString
from toptica.lasersdk.asyncio.client import DecopBinary

from toptica.lasersdk.asyncio.client import MutableDecopBoolean
from toptica.lasersdk.asyncio.client import MutableDecopInteger
from toptica.lasersdk.asyncio.client import MutableDecopReal
from toptica.lasersdk.asyncio.client import MutableDecopString
from toptica.lasersdk.asyncio.client import MutableDecopBinary

from toptica.lasersdk.asyncio.client import SettableDecopBoolean
from toptica.lasersdk.asyncio.client import SettableDecopInteger
from toptica.lasersdk.asyncio.client import SettableDecopReal
from toptica.lasersdk.asyncio.client import SettableDecopString
from toptica.lasersdk.asyncio.client import SettableDecopBinary


@pytest.fixture
def client():
    return AsyncMock(spec=Client)


@pytest.fixture
def subscription(client):
    return Subscription(client, 'param-name')


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_type, return_value", [(DecopBoolean, True),   (MutableDecopBoolean, True),   (SettableDecopBoolean, True),
                                  (DecopInteger, 7),      (MutableDecopInteger, 7),      (SettableDecopInteger, 7),
                                  (DecopReal,    2.7182), (MutableDecopReal,    2.7182), (SettableDecopReal,    2.7182),
                                  (DecopString,  'abc'),  (MutableDecopString,  'abc'),  (SettableDecopString,  'abc'),
                                  (DecopBinary,  b'xyz'), (MutableDecopBinary,  b'xyz'), (SettableDecopBinary,  b'xyz')]
)
async def test_get_calls_client_get(client_type, return_value):
    """Test if querying a parameter calls the get-method of the client."""
    client = AsyncMock(spec=Client, **{'get.return_value': return_value})

    param = client_type(client, 'param-name')
    result = await param.get()

    assert result == return_value
    client.get.assert_called_once_with('param-name', type(return_value))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_type, return_value", [(SettableDecopBoolean, True),
                                  (SettableDecopInteger, 7),
                                  (SettableDecopReal,    2.7182),
                                  (SettableDecopString,  'abc'),
                                  (SettableDecopBinary,  b'xyz')]
)
async def test_get_set_value_calls_client_get_set_value(client_type, return_value):
    """Test if querying a parameter calls the get-method of the client."""
    client = AsyncMock(spec=Client, **{'get_set_value.return_value': return_value})

    param = client_type(client, 'param-name')
    result = await param.get_set_value()

    assert result == return_value
    client.get_set_value.assert_called_once_with('param-name', type(return_value))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_type, value", [(MutableDecopBoolean, True),             (SettableDecopBoolean, True),
                           (MutableDecopInteger, 7),                 (SettableDecopInteger, 7),
                           (MutableDecopReal,    2),                 (SettableDecopReal,    2),
                           (MutableDecopReal,    2.7182),            (SettableDecopReal,    2.7182),
                           (MutableDecopString,  'abc'),             (SettableDecopString,  'abc'),
                           (MutableDecopBinary,  b'xyz'),            (SettableDecopBinary,  b'xyz'),
                           (MutableDecopBinary,  bytearray(b'uvw')), (SettableDecopBinary,  bytearray(b'uvw'))]
)
async def test_set_calls_client_set(client_type, value):
    """Test if setting a parameter calls the set-method of the client."""
    client = AsyncMock(spec=Client, **{'set.return_value': 7})

    param = client_type(client, 'param-name')
    result = await param.set(value)

    assert result == 7
    client.set.assert_called_once_with('param-name', value)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_type, value", [(MutableDecopBoolean, 7),      (SettableDecopBoolean, 7),
                           (MutableDecopInteger, 'abc'),  (SettableDecopInteger, 'abc'),
                           (MutableDecopReal,    b'xyz'), (SettableDecopReal,    b'xyz'),
                           (MutableDecopString,  2.7182), (SettableDecopString,  2.7182),
                           (MutableDecopBinary,  True),   (SettableDecopBinary,  True)]
)
async def test_set_with_invalid_type(client, client_type, value):
    """Test if setting a parameter value with an invalid type raises an AssertionError."""
    param = client_type(client, 'param-name')

    with pytest.raises(AssertionError):
        await param.set(value)

    client.set.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_type, py_type", [(DecopBoolean, bool),  (MutableDecopBoolean, bool),  (SettableDecopBoolean, bool),
                             (DecopInteger, int),   (MutableDecopInteger, int),   (SettableDecopInteger, int),
                             (DecopReal,    float), (MutableDecopReal,    float), (SettableDecopReal,    float),
                             (DecopString,  str),   (MutableDecopString,  str),   (SettableDecopString,  str),
                             (DecopBinary,  bytes), (MutableDecopBinary,  bytes), (SettableDecopBinary,  bytes)]
)
async def test_subscribe_calls_client_subscribe(subscription, client_type, py_type):
    """Test if subscribing to a parameter calls the subscribe-method of the client."""
    client = AsyncMock(spec=Client, **{'subscribe.return_value': subscription})

    param = client_type(client, 'param-name')
    result = await param.subscribe()

    assert result == subscription
    client.subscribe.assert_called_once_with('param-name', py_type)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client_type", [DecopBoolean, MutableDecopBoolean, SettableDecopBoolean,
                    DecopInteger, MutableDecopInteger, SettableDecopInteger,
                    DecopReal,    MutableDecopReal,    SettableDecopReal,
                    DecopString,  MutableDecopString,  SettableDecopString,
                    DecopBinary,  MutableDecopBinary,  SettableDecopBinary]
)
async def test_name_returns_init_value(client, client_type):
    """Test if the name-property of a parameter returns the provided value."""
    param = client_type(client, 'param-name')
    assert param.name == 'param-name'
