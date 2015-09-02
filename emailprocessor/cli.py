#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Command line interface"""

from __future__ import print_function

import click


@click.group()
def emailprocessor():
    """Simple SMTP server for processing emails"""
    pass


if __name__ == '__main__':
    emailprocessor()
