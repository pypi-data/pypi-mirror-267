import asyncio
import pytest

from toptica.lasersdk.client import Client
from toptica.lasersdk.client import DecopError
from toptica.lasersdk.client import UserLevel

from toptica.lasersdk.asyncio.connection import Connection


class MockConnection(Connection):
    def __init__(self, responses=None):
        if responses is None:
            responses = []
        self.responses = responses
        self.index = 0
        self.command_line = []
        self.monitoring_line = []
        self.opened = False
        self.closed = False

    async def open(self) -> None:
        self.opened = True

    async def close(self) -> None:
        self.closed = True

    async def read_command_line(self) -> str:
        self.index += 1
        return self.responses[self.index - 1]

    async def write_command_line(self, message: str) -> None:
        self.command_line.append(message)

    async def read_monitoring_line(self) -> str:
        await asyncio.sleep(5)
        return ''

    async def write_monitoring_line(self, message: str) -> None:
        return self.monitoring_line.append(message)

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
        return True

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return asyncio.get_event_loop()


# --- Client.get --------------------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("test, expected", [('#t', True), ('#f', False)])
def test_param_ref_bool(test, expected):

    connection = MockConnection([test])

    with Client(connection) as client:
        result = client.get('param-name', bool)

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == "(param-ref 'param-name)\n"
    assert isinstance(result, bool)
    assert result == expected


@pytest.mark.parametrize("test, expected", [('#t', True), ('#f', False)])
def test_param_gsv_bool(test, expected):

    connection = MockConnection([test])

    with Client(connection) as client:
        result = client.get_set_value('param-name', bool)

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == "(param-gsv 'param-name)\n"
    assert isinstance(result, bool)
    assert result is expected


def test_param_ref_atomic():

    connection = MockConnection(['(#t 5 2.5 "test" "YWQgYXN0cmEgcGVyIGFzcGVyYQ==")'])

    with Client(connection) as client:
        result = client.get('param-name', bool, int, float, str, bytes)

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == "(param-ref 'param-name)\n"
    assert isinstance(result, tuple)
    assert result[0] is True
    assert result[1] == 5
    assert result[2] == 2.5
    assert result[3] == 'test'
    assert result[4] == b'ad astra per aspera'


@pytest.mark.parametrize("test, expected", [
    ('(#t 5 1.2)', (bool, int)), ('(#t 5 1.2)', (bool, int, float, str)),
])
def test_param_ref_atomic_error(test, expected):

    connection = MockConnection([test])

    with pytest.raises(DecopError):
        with Client(connection) as client:
            client.get('param-name', *expected)


@pytest.mark.parametrize("test, expected", [
    ('#t', True), ('100', 100), ('3.1415', 3.1415), ('"xyz"', 'xyz')
])
def test_param_ref_inferred(test, expected):

    connection = MockConnection([test])

    with Client(connection) as client:
        result = client.get('param-name')

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == "(param-ref 'param-name)\n"
    assert isinstance(result, type(expected))
    assert result == expected


def test_param_ref_atomic_inferred():

    connection = MockConnection(['(#t 5 2.5 "test" &YWQgYXN0cmEgcGVyIGFzcGVyYQ==)'])

    with Client(connection) as client:
        result = client.get('param-name')

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == "(param-ref 'param-name)\n"
    assert isinstance(result, tuple)
    assert result[0] is True
    assert result[1] == 5
    assert result[2] == 2.5
    assert result[3] == 'test'
    assert result[4] == b'ad astra per aspera'


# --- Client.get_set_value ----------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("test, expected", [
    ('#t', True), ('100', 100), ('3.1415', 3.1415), ('"xyz"', 'xyz'), ('&YWQgYXN0cmEgcGVyIGFzcGVyYQ==', b'ad astra per aspera')
])
def test_get_set_value(test, expected):

    connection = MockConnection([test])

    with Client(connection) as client:
        result = client.get_set_value('param-name', type(expected))

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == "(param-gsv 'param-name)\n"
    assert isinstance(result, type(expected))
    assert result == expected


@pytest.mark.parametrize("test, expected", [
    ('#t', True), ('100', 100), ('3.1415', 3.1415), ('"xyz"', 'xyz'), ('&YWQgYXN0cmEgcGVyIGFzcGVyYQ==', b'ad astra per aspera')
])
def test_get_set_value_inferred(test, expected):

    connection = MockConnection([test])

    with Client(connection) as client:
        result = client.get_set_value('param-name')

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == "(param-gsv 'param-name)\n"
    assert isinstance(result, type(expected))
    assert result == expected


def test_get_set_value_atomic():

    connection = MockConnection(['(#t 5 2.5 "test" "YWQgYXN0cmEgcGVyIGFzcGVyYQ==")'])

    with Client(connection) as client:
        result = client.get_set_value('param-name', bool, int, float, str, bytes)

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == "(param-gsv 'param-name)\n"
    assert isinstance(result, tuple)
    assert result[0] is True
    assert result[1] == 5
    assert result[2] == 2.5
    assert result[3] == 'test'
    assert result[4] == b'ad astra per aspera'


def test_get_set_value_atomic_inferred():

    connection = MockConnection(['(#t 5 2.5 "test" &YWQgYXN0cmEgcGVyIGFzcGVyYQ==)'])

    with Client(connection) as client:
        result = client.get_set_value('param-name')

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == "(param-gsv 'param-name)\n"
    assert isinstance(result, tuple)
    assert result[0] is True
    assert result[1] == 5
    assert result[2] == 2.5
    assert result[3] == 'test'
    assert result[4] == b'ad astra per aspera'


@pytest.mark.parametrize("test, expected", [
    ('(#t 5 1.2)', (bool, int)), ('(#t 5 1.2)', (bool, int, float, str)),
])
def test_get_set_value_atomic_error(test, expected):

    connection = MockConnection([test])

    with pytest.raises(DecopError):
        with Client(connection) as client:
            client.get_set_value('param-name', *expected)


# --- Client.set --------------------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("test, expected", [(True, "(param-set! 'param-name #t)\n"), (False, "(param-set! 'param-name #f)\n")])
def test_param_set_bool(test, expected):

    connection = MockConnection(['5'])

    with Client(connection) as client:
        result = client.set('param-name', test)

    assert result == 5

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == expected


def test_param_set_atomic():

    connection = MockConnection(['5'])

    with Client(connection) as client:
        result = client.set('param-name', True, 5, 2.5, 'test', b'ad astra per aspera')

    assert result == 5

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == "(param-set! 'param-name '(#t 5 2.5 \"test\" \"YWQgYXN0cmEgcGVyIGFzcGVyYQ==\"))\n"


# --- Client.exec -------------------------------------------------------------
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("test, expected",
                         [([], "(exec 'command-name)\n"), ([1], "(exec 'command-name 1)\n"),
                          ([1.234, 'astra'], "(exec 'command-name 1.234 \"astra\")\n")])
def test_exec(test, expected):

    connection = MockConnection(['()'])

    with Client(connection) as client:
        client.exec('command-name', *test)

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == expected


@pytest.mark.parametrize("test, expected",
                         [('baba', ["(exec 'command-name)\n", "baba#"]),
                          (b'baba', ["(exec 'command-name)\n", "YmFiYQ==#"])])
def test_exec_inputstream(test, expected):

    connection = MockConnection(['()'])

    with Client(connection) as client:
        client.exec('command-name', input_stream=test)

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == expected[0]
    assert connection.command_line[1] == expected[1]


@pytest.mark.parametrize("test, expected, t",
                         [('()', '', str), ('baba\n()', 'baba\n', str), ('()', b'', bytes),
                          ('YmFiYQ==#\n()', b'baba', bytes), ('YmFi\nYQ==#\n()', b'baba', bytes)])
def test_exec_output_type(test, expected, t):

    connection = MockConnection([test])

    with Client(connection) as client:
        output = client.exec('command-name', output_type=t)

    assert output == expected


@pytest.mark.parametrize("test, expected, t", [('2.71828', 2.71828, float), ('5', 5, int), ('"baba"', 'baba', str)])
def test_exec_return_type(test, expected, t):

    connection = MockConnection([test])

    with Client(connection) as client:
        ret = client.exec('command-name', return_type=t)

    assert ret == expected


@pytest.mark.parametrize("out_test, out_expected, out_t",
                         [('baba', 'baba\n', str), ('YmFiYQ==#\n()', b'baba', bytes), ('YmFi\nYQ==#', b'baba', bytes)])
@pytest.mark.parametrize("ret_test, ret_expected, ret_t",
                         [('2.71828', 2.71828, float), ('5', 5, int), ('"baba"', 'baba', str)])
def test_exec_output_type_return_type(out_test, out_expected, out_t, ret_test, ret_expected, ret_t):

    connection = MockConnection([out_test + '\n' + ret_test])

    with Client(connection) as client:
        out, ret = client.exec('command-name', output_type=out_t, return_type=ret_t)

    assert out == out_expected
    assert ret == ret_expected


@pytest.mark.parametrize("test, expected",
                         [('', "Missing response for command 'command-name'")])
def test_exec_missing_response(test, expected):

    connection = MockConnection([test])

    with pytest.raises(DecopError) as exc:
        with Client(connection) as client:
            client.exec('command-name')

    assert str(exc.value) == expected


@pytest.mark.parametrize("test, expected",
                         [('Error: -1 Unexpected', 'Error: -1 Unexpected')])
def test_exec_single_line_error(test, expected):

    connection = MockConnection([test])

    with pytest.raises(DecopError) as exc:
        with Client(connection) as client:
            client.exec('command-name')

    assert str(exc.value) == expected


@pytest.mark.parametrize("test, expected",
                         [('Error: -1 Line 1\nLine 2', 'Error: -1 Line 1\nLine 2'),
                          ('Error: -1 Line 1\nLine 2\nLine 3', 'Error: -1 Line 1\nLine 2\nLine 3')])
def test_exec_multi_line_error(test, expected):

    connection = MockConnection([test])

    with pytest.raises(DecopError) as exc:
        with Client(connection) as client:
            client.exec('command-name')

    assert str(exc.value) == expected


@pytest.mark.parametrize("test, expected",
                         [('Valid Data\nError: -1 Message', 'Error: -1 Message'),
                          ('Valid Data 1\nValid Data 2\nError: -1 Message', 'Error: -1 Message')])
def test_exec_data_before_single_line_error(test, expected):

    connection = MockConnection([test])

    with pytest.raises(DecopError) as exc:
        with Client(connection) as client:
            client.exec('command-name')

    assert str(exc.value) == expected


@pytest.mark.parametrize("test, cmd_req, cmd_resp, mon_req, expected",
                         [(UserLevel.READONLY, '(exec \'change-ul 4 "")\n', "4", '(change-ul 4 "")\n', UserLevel.READONLY),
                          (UserLevel.NORMAL,   '(exec \'change-ul 3 "")\n', "3", '(change-ul 3 "")\n', UserLevel.NORMAL)])
def test_change_ul_empty_password_success(test, cmd_req, cmd_resp, mon_req, expected):

    connection = MockConnection([cmd_resp])

    with Client(connection) as client:
        result = client.change_ul(test, '')

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == cmd_req
    assert connection.monitoring_line[0] == mon_req

    assert isinstance(result, UserLevel)
    assert result is expected


@pytest.mark.parametrize("test, cmd_req, cmd_resp, mon_req, expected",
                         [(UserLevel.READONLY, '(exec \'change-ul 4 "")\n', "4", '(change-ul 4 "")\n', UserLevel.READONLY),
                          (UserLevel.NORMAL,   '(exec \'change-ul 3 "")\n', "3", '(change-ul 3 "")\n', UserLevel.NORMAL)])
def test_change_ul_no_password_success(test, cmd_req, cmd_resp, mon_req, expected):

    connection = MockConnection([cmd_resp])

    with Client(connection) as client:
        result = client.change_ul(test)

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == cmd_req
    assert connection.monitoring_line[0] == mon_req

    assert isinstance(result, UserLevel)
    assert result is expected


@pytest.mark.parametrize("test", [UserLevel.MAINTENANCE, UserLevel.SERVICE, UserLevel.INTERNAL])
def test_change_ul_empty_password_failure(test):

    connection = MockConnection(['3'])

    with Client(connection) as client:
        result = client.change_ul(test, '')

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == "(param-ref 'ul)\n"
    assert len(connection.monitoring_line) == 0

    assert isinstance(result, UserLevel)
    assert result is UserLevel.NORMAL


@pytest.mark.parametrize("test", [UserLevel.MAINTENANCE, UserLevel.SERVICE, UserLevel.INTERNAL])
def test_change_ul_no_password_failure(test):

    connection = MockConnection(['3'])

    with Client(connection) as client:
        result = client.change_ul(test)

    assert connection.opened is True
    assert connection.closed is True

    assert connection.command_line[0] == "(param-ref 'ul)\n"
    assert len(connection.monitoring_line) == 0

    assert isinstance(result, UserLevel)
    assert result is UserLevel.NORMAL


def test_run_timeout():

    connection = MockConnection(['3'])

    with Client(connection) as client:
        client.run(timeout=1)


def test_cancel_last_subscription():

    connection = MockConnection()

    with Client(connection) as client:
        subscription = client.subscribe('uptime', str, lambda: None)
        subscription.cancel()

    assert len(connection.monitoring_line) == 2

    assert connection.monitoring_line[0] == "(add 'uptime)\n"
    assert connection.monitoring_line[1] == "(remove 'uptime)\n"


def test_cancel_subscription_on_close():

    connection = MockConnection()

    with Client(connection) as client:
        client.subscribe('uptime', str, lambda: None)

    with Client(connection) as client:
        client.subscribe('uptime', str, lambda: None)

    assert len(connection.monitoring_line) == 4

    assert connection.monitoring_line[0] == "(add 'uptime)\n"
    assert connection.monitoring_line[1] == "(remove 'uptime)\n"
    assert connection.monitoring_line[2] == "(add 'uptime)\n"
    assert connection.monitoring_line[3] == "(remove 'uptime)\n"


def test_run_callback_1():

    connection = MockConnection(['3'])

    with Client(connection) as client:
        subscription = client.subscribe('uptime', str, lambda: None)
        subscription.cancel()

    assert len(connection.monitoring_line) == 2

    assert connection.monitoring_line[0] == "(add 'uptime)\n"
    assert connection.monitoring_line[1] == "(remove 'uptime)\n"


def test_run_callback_2():

    connection = MockConnection(['3'])

    with Client(connection) as client:
        subscription1 = client.subscribe('uptime', str, lambda: None)
        subscription2 = client.subscribe('uptime', str, lambda: None)
        subscription1.cancel()
        subscription2.cancel()

    assert len(connection.monitoring_line) == 2

    assert connection.monitoring_line[0] == "(add 'uptime)\n"
    assert connection.monitoring_line[1] == "(remove 'uptime)\n"


def test_run_callback_3():

    connection = MockConnection(['3'])

    with Client(connection) as client:
        subscription = client.subscribe('uptime', str, lambda: None)
        subscription.cancel()
        subscription = client.subscribe('uptime', str, lambda: None)
        subscription.cancel()

    assert len(connection.monitoring_line) == 4

    assert connection.monitoring_line[0] == "(add 'uptime)\n"
    assert connection.monitoring_line[1] == "(remove 'uptime)\n"
    assert connection.monitoring_line[2] == "(add 'uptime)\n"
    assert connection.monitoring_line[3] == "(remove 'uptime)\n"


def test_run_callback_4():

    connection = MockConnection(['3'])

    with Client(connection) as client:
        client.subscribe('uptime', str, lambda: None)

    assert len(connection.monitoring_line) == 2

    assert connection.monitoring_line[0] == "(add 'uptime)\n"
    assert connection.monitoring_line[1] == "(remove 'uptime)\n"


def test_run_callback_5():

    connection = MockConnection(['3'])

    with Client(connection) as client:
        subscription = client.subscribe('uptime', str, lambda: None)
        subscription.cancel()

    with Client(connection) as client:
        subscription = client.subscribe('uptime', str, lambda: None)
        subscription.cancel()

    assert len(connection.monitoring_line) == 4

    assert connection.monitoring_line[0] == "(add 'uptime)\n"
    assert connection.monitoring_line[1] == "(remove 'uptime)\n"
    assert connection.monitoring_line[2] == "(add 'uptime)\n"
    assert connection.monitoring_line[3] == "(remove 'uptime)\n"


def test_run_callback_6():

    connection = MockConnection(['3'])

    with Client(connection) as client:
        client.subscribe('uptime', lambda: None, str)

    with Client(connection) as client:
        client.subscribe('uptime', lambda: None, str)

    assert len(connection.monitoring_line) == 4

    assert connection.monitoring_line[0] == "(add 'uptime)\n"
    assert connection.monitoring_line[1] == "(remove 'uptime)\n"
    assert connection.monitoring_line[2] == "(add 'uptime)\n"
    assert connection.monitoring_line[3] == "(remove 'uptime)\n"
