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
    yield 'email_summary'


class TestCli():
    @parametrize('helparg', ['--help'])
    def test_help(self, helparg, runner):
        result = runner.invoke(emailprocessor, [helparg])
        assert result.exit_code == 0
        assert 'emailprocessor' in result.output
