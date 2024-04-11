import asyncio

from toptica.lasersdk.dlcpro.v1_7_0 import DLCpro, Connection


class MockConnection(Connection):
    def __init__(self, responses):
        self.responses = responses
        self.requests = []
        self.index = 0

    async def open(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def read_command_line(self) -> str:
        self.index += 1
        return self.responses[self.index - 1]

    async def write_command_line(self, message: str) -> None:
        self.requests.append(message)

    async def read_monitoring_line(self) -> str:
        raise NotImplementedError

    async def write_monitoring_line(self, message: str) -> None:
        raise NotImplementedError

    @property
    def timeout(self) -> float:
        return 1.0

    @property
    def is_open(self) -> bool:
        return True

    @property
    def command_line_available(self) -> bool:
        return True

    @property
    def monitoring_line_available(self) -> bool:
        return False

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return asyncio.get_event_loop()


def test_param_ref_device_class():
    connection = MockConnection(['#t'])
    with DLCpro(connection) as dlc:
        assert dlc.emission.get() is True
        assert connection.requests == ["(param-ref 'emission)\n"]


def test_param_set_device_class():
    connection = MockConnection(['0'])
    with DLCpro(connection) as dlc:
        dlc.system_label.set('SYZYGY')
        assert connection.requests == ["(param-set! 'system-label \"SYZYGY\")\n"]


def test_cmd_device_class():
    connection = MockConnection(['0'])
    with DLCpro(connection) as dlc:
        dlc.change_password('Pismis24')
        assert connection.requests == ["(exec 'change-password \"Pismis24\")\n"]


def test_param_ref_typedef():
    connection = MockConnection(['"Scorpius"'])
    with DLCpro(connection) as dlc:
        assert dlc.laser1.dl.type.get() == 'Scorpius'
        assert connection.requests == ["(param-ref 'laser1:dl:type)\n"]


def test_param_set_typedef():
    connection = MockConnection(['0'])
    with DLCpro(connection) as dlc:
        dlc.laser1.dl.lock.lock_without_lockpoint.set(True)
        assert connection.requests == ["(param-set! 'laser1:dl:lock:lock-without-lockpoint #t)\n"]


def test_cmd_typedef():
    connection = MockConnection(['0'])
    with DLCpro(connection) as dlc:
        dlc.laser1.dl.lock.close()
        assert connection.requests == ["(exec 'laser1:dl:lock:close)\n"]
