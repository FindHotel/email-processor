#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Command line interface"""

from __future__ import print_function

import click


@click.group()
def emailprocessor():
    """Program entry point.

    :param command: Name of a {project} command
    :type command: str
    :param argv: Parameters to pass to the command
    "type command: :class:`list`
    """
    pass


if __name__ == '__main__':
    emailprocessor()
