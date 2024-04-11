import pytest

from mock import MagicMock
from datetime import datetime

from toptica.lasersdk.client import Client
from toptica.lasersdk.client import Subscription


@pytest.fixture
def client():
    return MagicMock(spec=Client)


@pytest.fixture
def callback():
    return MagicMock()


@pytest.fixture
def timestamp():
    return datetime.now()


@pytest.fixture
def error():
    return RuntimeError()


def test_update_value(client, callback, timestamp):
    """Test if updating a subscription will invoke the callback."""
    subscription = Subscription(client, 'param-name', callback)

    subscription.update(timestamp, 1024)

    callback.assert_called_once_with(subscription, timestamp, 1024)


def test_update_value_with_error(client, callback, timestamp, error):
    """Test if updating a subscription will invoke the callback (including errors)."""
    subscription = Subscription(client, 'param-name', callback)

    subscription.update(timestamp, error)

    callback.assert_called_once_with(subscription, timestamp, error)


def test_update_value_when_cancelled(client, callback, timestamp):
    """Test if cancelling a subscription will prevent invoking the callback."""
    subscription = Subscription(client, 'param-name', callback)

    subscription.cancel()
    subscription.update(timestamp, 1024)

    callback.assert_not_called()


def test_update_value_inside_of_context(client, callback, timestamp):
    """Test if updating a subscription inside of a context will invoke the callback."""
    with Subscription(client, 'param-name', callback) as subscription:
        subscription.update(timestamp, 1024)

    callback.assert_called_once_with(subscription, timestamp, 1024)


def test_update_value_outside_of_context(client, callback, timestamp):
    """Test if updating a subscription outside of a context will prevent invoking the callback."""
    with Subscription(client, 'param-name', callback) as subscription:
        pass

    subscription.update(timestamp, 1024)

    callback.assert_not_called()


def test_cancel_subscription(client, callback):
    """Test if cancelling a subscription will unsubscribe it from the client."""
    subscription = Subscription(client, 'param-name', callback)

    subscription.cancel()

    client.unsubscribe.assert_called_once_with(subscription)


def test_cancel_subscription_only_once(client, callback):
    """Test if cancelling a subscription multiple times will unsubscribe it from the client only once."""
    subscription = Subscription(client, 'param-name', callback)

    subscription.cancel()
    subscription.cancel()  # Second cancellation shouldn't do anything

    client.unsubscribe.assert_called_once_with(subscription)


def test_context_manager_cancels_subscription(client, callback):
    """Test if using a context manager will cancel the subscription."""
    with Subscription(client, 'param-name', callback) as subscription:
        pass

    client.unsubscribe.assert_called_once_with(subscription)


def test_context_manager_cancels_subscription_only_once(client, callback):
    """Test if using a context manager will cancel the subscription only once."""
    with Subscription(client, 'param-name', callback) as subscription:
        pass

    subscription.cancel()  # Second cancellation shouldn't do anything

    client.unsubscribe.assert_called_once_with(subscription)


def test_name_returns_init_value(client, callback):
    """Test if the name-property of a subscription returns the provided value."""
    subscription = Subscription(client, 'param-name', callback)
    assert subscription.name == 'param-name'
