# -*- coding: utf-8 -*-

# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#
import pytest
parametrize = pytest.mark.parametrize

from emailprocessor.cli import emailprocessor
from click.testing import CliRunner


class TestCli(object):
    @parametrize('helparg', ['--help'])
    def test_help(self, helparg, capsys):
        runner = CliRunner()
        result = runner.invoke(emailprocessor, [helparg])
        assert result.exit_code == 0
        assert 'emailprocessor' in result.output
