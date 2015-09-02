#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Command line interface"""

from __future__ import print_function

import click
import emailprocessor.basic as basic


@click.group()
@click.pass_context
@click.option('--address', default='127.0.0.1')
@click.option('--port', default=1025)
def emailprocessor(ctx, address, port):
    """Simple SMTP server for processing emails"""
    ctx.obj = {'address': address, 'port': port}


@emailprocessor.command()
@click.pass_context
def email_summary(ctx):
    """Prints a summary of the email"""
    server = basic.PrintSummarySMTPServer((ctx.obj['address'],
                                           ctx.obj['port']), None)
    server.run()


@emailprocessor.command()
@click.pass_context
def save_attachments(ctx):
    """Saves email attachments"""
    server = basic.SaveAttachmentsSMTPServer((ctx.obj['address'],
                                              ctx.obj['port']), None)
    server.run()


if __name__ == '__main__':
    emailprocessor()
