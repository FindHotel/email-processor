# -*- coding: utf-8 -*-

# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#
import pytest
parametrize = pytest.mark.parametrize

from emailprocessor.cli import emailprocessor
from click.testing import CliRunner


@pytest.yield_fixture(scope="module")
def runner():
    yield CliRunner()


@pytest.yield_fixture(scope="module")
def command():
    yield emailprocessor.list_commands(None)[0]


class TestCli():
    @parametrize('helparg', ['--help'])
    def test_help(self, helparg, runner):
        result = runner.invoke(emailprocessor, [helparg])
        assert result.exit_code == 0
        assert 'emailprocessor' in result.output

    @parametrize('addrarg', ['--address', '-a'])
    @parametrize('portarg', ['--port', '-p'])
    @parametrize('debugarg', ['--debug', '--no-debug'])
    def test_address(self, addrarg, portarg, debugarg, runner, command):
        result = runner.invoke(
            emailprocessor,
            ['--timeout', 1, addrarg, '127.0.0.1',
             portarg, 1027, debugarg, command])
        assert result.exit_code == 0
        assert '127.0.0.1' in result.output
