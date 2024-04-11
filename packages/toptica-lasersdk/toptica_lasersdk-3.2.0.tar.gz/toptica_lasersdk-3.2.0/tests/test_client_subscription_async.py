import pytest

from mock import AsyncMock
from datetime import datetime

from toptica.lasersdk.asyncio.client import Client
from toptica.lasersdk.asyncio.client import Subscription
from toptica.lasersdk.asyncio.client import SubscriptionValue
from toptica.lasersdk.asyncio.client import DecopError


@pytest.fixture
def client():
    return AsyncMock(spec=Client)


@pytest.fixture
def timestamp():
    return datetime.now()


@pytest.fixture
def error():
    return RuntimeError()


@pytest.mark.asyncio
async def test_cancel_subscription(client):
    """Test if cancelling a subscription will unsubscribe it from the client."""
    subscription = Subscription(client, 'param-name')

    await subscription.cancel()

    client.unsubscribe.assert_called_once_with(subscription)


@pytest.mark.asyncio
async def test_cancel_subscription_only_once(client):
    """Test if cancelling a subscription multiple times will unsubscribe it from the client only once."""
    subscription = Subscription(client, 'param-name')

    await subscription.cancel()
    await subscription.cancel()  # Second cancellation shouldn't do anything

    client.unsubscribe.assert_called_once_with(subscription)


@pytest.mark.asyncio
async def test_context_manager_cancels_subscription(client):
    """Test if using a context manager will cancel the subscription."""
    async with Subscription(client, 'param-name') as subscription:
        pass

    client.unsubscribe.assert_called_once_with(subscription)


@pytest.mark.asyncio
async def test_context_manager_cancels_subscription_only_once(client):
    """Test if using a context manager will cancel the subscription only once."""
    async with Subscription(client, 'param-name') as subscription:
        pass

    await subscription.cancel()  # Second cancellation shouldn't do anything

    client.unsubscribe.assert_called_once_with(subscription)


@pytest.mark.asyncio
async def test_name_returns_init_value(client):
    """Test if the name-property of a subscription returns the provided value."""
    subscription = Subscription(client, 'param-name')
    assert subscription.name == 'param-name'


@pytest.mark.asyncio
async def test_iteration_when_canceled_1(client):
    """Test if iterating a canceled subscription succeeds."""
    async with Subscription(client, 'param-name') as subscription:
        await subscription.cancel()
        async for _ in subscription:
            assert False  # Should not be called


@pytest.mark.asyncio
async def test_iterating_when_canceled_2(client):
    """Test if iterating a canceled subscription succeeds."""
    async with Subscription(client, 'param-name') as subscription:

        now = datetime.now()
        await subscription.update(now, SubscriptionValue('value-str'))

        async for timestamp, value in subscription:
            assert timestamp == now
            assert value == 'value-str'

            await subscription.cancel()


@pytest.mark.asyncio
async def test_awaiting_subscription(client):
    """Test if a subscription can be awaited for the next value."""
    async with Subscription(client, 'param-name') as subscription:

        now = datetime.now()
        await subscription.update(now, SubscriptionValue('value-str'))

        timestamp, value = await subscription

        assert timestamp == now
        assert value == 'value-str'


@pytest.mark.asyncio
async def test_awaiting_next_value(client):
    """Test if the next value can be awaited."""
    async with Subscription(client, 'param-name') as subscription:

        now = datetime.now()
        await subscription.update(now, SubscriptionValue('value-str'))

        timestamp, value = await subscription.next()

        assert timestamp == now
        assert value == 'value-str'


@pytest.mark.asyncio
async def test_fail_awaiting_subscription(client):
    """Test if awaiting a value raises an exception when canceled."""
    subscription = Subscription(client, 'param-name')
    await subscription.cancel()

    with pytest.raises(DecopError):
        await subscription

    with pytest.raises(DecopError):
        await subscription.next()


@pytest.mark.asyncio
async def test_raise_exception_from_update(client):
    """Test if awaiting a value raises the exception from an update."""
    async with Subscription(client, 'param-name') as subscription:

        await subscription.update(datetime.now(), SubscriptionValue(DecopError('Something went wrong...')))

        with pytest.raises(DecopError):
            await subscription

        #
        await subscription.update(datetime.now(), SubscriptionValue(DecopError('{#`%$)%&`+${`%&')))

        with pytest.raises(DecopError):
            await subscription.next()

        #
        await subscription.update(datetime.now(), SubscriptionValue(DecopError('NO CARRIER')))

        with pytest.raises(DecopError):
            async for _ in subscription:
                assert False  # Should never be called
