import asyncio
import pytest

from toptica.lasersdk.asyncio.connection import *
from utils import LoopbackServer


@pytest.mark.asyncio
async def test_calling_methods_when_closed():

    net = NetworkConnection('localhost')

    with pytest.raises(UnavailableError):
        await net.write_command_line('')

    with pytest.raises(UnavailableError):
        await net.read_command_line()

    with pytest.raises(UnavailableError):
        await net.write_monitoring_line('')

    with pytest.raises(UnavailableError):
        await net.read_monitoring_line()


@pytest.mark.asyncio
async def test_status_when_closed():

    net = NetworkConnection('localhost')

    assert not net.is_open
    assert not net.command_line_available
    assert not net.monitoring_line_available


@pytest.mark.asyncio
async def test_invalid_ip_address():
    with pytest.raises(DeviceNotFoundError):
        net = NetworkConnection('127.0.0.256', timeout=1)
        await net.open()


@pytest.mark.asyncio
async def test_unavailable_dns_host():
    with pytest.raises(DeviceNotFoundError):
        net = NetworkConnection('dlcpro.example.com', timeout=1)
        await net.open()


@pytest.mark.asyncio
async def test_unavailable_serial_number():
    with pytest.raises(DeviceNotFoundError):
        net = NetworkConnection('ScienceRack-00:1F:7B:15:6F:XY', timeout=1)
        await net.open()


@pytest.mark.asyncio
async def test_missing_welcome_message():
    async with LoopbackServer(send_welcome_message=False) as server:
        net = NetworkConnection(server.host, command_line_port=server.command_line_port, monitoring_line_port=0, timeout=1)

        with pytest.raises(DeviceNotFoundError):
            await net.open()

        assert not net.is_open
        assert not net.command_line_available
        assert not net.monitoring_line_available


@pytest.mark.asyncio
@pytest.mark.parametrize('prompt', ['\r\n> ', '\n> '])
async def test_canonical_read_and_write_to_command_line(prompt):
    async with LoopbackServer() as server:
        async with NetworkConnection(server.host, command_line_port=server.command_line_port, monitoring_line_port=0) as net:

            await net.write_command_line("(param-ref 'uptime-txt)\n")
            await server.send_command_line_response('"1508:37:20"' + prompt)

            response = await net.read_command_line()

        assert await server.command_line_requests.get() == b"(param-ref 'uptime-txt)\n"
        assert response == '"1508:37:20"'


@pytest.mark.asyncio
async def test_context_manager_1():
    """Test if the context manager support works as expected."""
    async with LoopbackServer() as server:
        async with NetworkConnection(server.host, command_line_port=server.command_line_port, monitoring_line_port=0) as net:
            assert net.is_open
            assert net.command_line_available
            assert not net.monitoring_line_available

        assert not net.is_open
        assert not net.command_line_available
        assert not net.monitoring_line_available


@pytest.mark.asyncio
async def test_context_manager_2():
    """Test if the context manager support works as expected."""
    async with LoopbackServer() as server:
        async with NetworkConnection(server.host, command_line_port=0, monitoring_line_port=server.monitoring_line_port) as net:
            assert net.is_open
            assert not net.command_line_available
            assert net.monitoring_line_available


@pytest.mark.asyncio
async def test_context_manager_3():
    """Test if the context manager support works as expected."""
    async with LoopbackServer() as server:
        async with NetworkConnection(server.host, command_line_port=server.command_line_port, monitoring_line_port=server.monitoring_line_port) as net:
            assert net.is_open
            assert net.command_line_available
            assert net.monitoring_line_available


@pytest.mark.asyncio
async def test_context_manager_4():
    """Test if the context manager support works as expected."""
    async with LoopbackServer() as server:
        async with NetworkConnection(server.host, command_line_port=0, monitoring_line_port=0) as net:
            assert not net.is_open
            assert not net.command_line_available
            assert not net.monitoring_line_available


@pytest.mark.asyncio
async def test_missing_ports():
    """Test if the connection fails gracefully when both ports are missing."""
    async with NetworkConnection('127.0.0.1', command_line_port=0, monitoring_line_port=0) as net:
        assert not net.is_open
        assert not net.command_line_available
        assert not net.monitoring_line_available


@pytest.mark.asyncio
async def test_properties_of_closed_connection():
    """Test if the properties of a closed connection are valid."""
    net = NetworkConnection('127.0.0.1')
    assert not net.is_open
    assert not net.command_line_available
    assert not net.monitoring_line_available


@pytest.mark.skip
@pytest.mark.asyncio
async def test_negative_timeout():
    """Test if a negative timeout raises an exception."""
    with pytest.raises(DecopError):
        NetworkConnection('127.0.0.1', timeout=-1)


@pytest.mark.asyncio
async def test_using_closed_command_line():
    """Test if using a closed command line raises an exception."""
    async with NetworkConnection('127.0.0.1', command_line_port=0, monitoring_line_port=0) as net:
        with pytest.raises(UnavailableError):
            await net.read_command_line()
        with pytest.raises(UnavailableError):
            await net.write_command_line("(param-ref 'uptime)")


@pytest.mark.asyncio
async def test_using_closed_monitoring_line():
    """Test if using a closed command line raises an exception."""
    async with NetworkConnection('127.0.0.1', command_line_port=0, monitoring_line_port=0) as net:
        with pytest.raises(UnavailableError):
            await net.read_monitoring_line()
        with pytest.raises(UnavailableError):
            await net.write_monitoring_line("(add 'uptime)")


@pytest.mark.asyncio
async def test_missing_client_1():
    """Test if connecting to a non existing device raises an exception."""
    net = NetworkConnection('127.0.0.255', command_line_port=1998, monitoring_line_port=0)

    with pytest.raises(DeviceNotFoundError):
        await net.open()


@pytest.mark.asyncio
async def test_missing_client_2():
    """Test if connecting to a non existing device raises an exception."""
    net = NetworkConnection('127.0.0.255', command_line_port=0, monitoring_line_port=1999)

    with pytest.raises(DeviceNotFoundError):
        await net.open()


@pytest.mark.asyncio
async def test_wrong_port_1():
    """Test if using a wrong port raises an exception."""
    async with LoopbackServer() as server:
        net = NetworkConnection(server.host, command_line_port=80, monitoring_line_port=0)
        with pytest.raises(DeviceNotFoundError):
            await net.open()


@pytest.mark.asyncio
async def test_wrong_port_2():
    """Test if using a wrong port raises an exception."""
    async with LoopbackServer() as server:
        net = NetworkConnection(server.host, command_line_port=0, monitoring_line_port=80)
        with pytest.raises(DeviceNotFoundError):
            await net.open()


@pytest.mark.skip
@pytest.mark.asyncio
async def test_read_commandline_with_client_close():
    """Test if closing the connection from the client side will raise an exception in read_command_line."""
    async with LoopbackServer() as server:
        async with NetworkConnection('127.0.0.1', server.command_line_port, monitoring_line_port=0) as net:
            with pytest.raises(ConnectionClosedError):
                await asyncio.gather(net.read_command_line(), net.close())


@pytest.mark.skip
@pytest.mark.asyncio
async def test_read_commandline_with_server_close():
    """Test if closing the connection from the server side will raise an exception in read_command_line."""
    async with LoopbackServer() as server:
        async with NetworkConnection('127.0.0.1', server.command_line_port, monitoring_line_port=0) as net:
            with pytest.raises(ConnectionClosedError):
                await asyncio.gather(net.read_command_line(), server.close())


@pytest.mark.asyncio
@pytest.mark.parametrize('connection', [NetworkConnection('127.0.0.1'), SerialConnection('loop://')])
async def test_no_new_event_loop(connection):
    """Test if connections create a new event loop (they shouldn't)."""
    with pytest.raises(DecopError):
        connection.loop.is_running()
