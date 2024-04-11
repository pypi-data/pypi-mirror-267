import pytest

from toptica.lasersdk import lasersdk_gen as gen
from toptica.lasersdk.decop import UserLevel


def test_empty():
    with pytest.raises(SystemExit):
        gen.process_command_line([])


def test_empty_with_option():
    with pytest.raises(SystemExit):
        gen.process_command_line(['--async'])


def test_single_file():
    args = gen.process_command_line(['the_file.xml'])

    assert args.model_xml == 'the_file.xml'
    assert args.module_name is None
    assert args.ul == UserLevel.NORMAL
    assert args.use_async is False
    assert args.download is False


@pytest.mark.parametrize("option", ['-ul', '--userlevel'])
@pytest.mark.parametrize("param", ['', '5'])
def test_ul_error(option, param):
    with pytest.raises(SystemExit):
        gen.process_command_line(['the_file.xml', option, param])


@pytest.mark.parametrize("option", ['-ul', '--userlevel'])
@pytest.mark.parametrize("param", ['0', '1', '2', '3', '4'])
def test_ul(option, param):
    args = gen.process_command_line(['the_file.xml', option, param])

    assert args.model_xml == 'the_file.xml'
    assert args.module_name is None
    assert args.ul == UserLevel(int(param))
    assert args.use_async is False
    assert args.download is False


@pytest.mark.parametrize("option", ['-a', '--async'])
def test_async(option):
    args = gen.process_command_line(['the_file.xml', option])

    assert args.model_xml == 'the_file.xml'
    assert args.module_name is None
    assert args.ul == UserLevel.NORMAL
    assert args.use_async is True
    assert args.download is False


@pytest.mark.parametrize("option", ['-d', '--download'])
def test_download(option):
    args = gen.process_command_line(['the_file.xml', option])

    assert args.model_xml == 'the_file.xml'
    assert args.module_name is None
    assert args.ul == UserLevel.NORMAL
    assert args.use_async is False
    assert args.download is True


@pytest.mark.parametrize("option", ['-m', '--module'])
def test_module(option):
    args = gen.process_command_line(['the_file.xml', option, 'module.py'])

    assert args.model_xml == 'the_file.xml'
    assert args.module_name == 'module.py'
    assert args.ul == UserLevel.NORMAL
    assert args.use_async is False
    assert args.download is False


@pytest.mark.parametrize("option", ['-m', '--module'])
def test_module_error(option):
    with pytest.raises(SystemExit):
        gen.process_command_line(['the_file.xml', option])
