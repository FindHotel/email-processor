#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Command line interface"""

from __future__ import print_function

import click
import emailprocessor.basic as basic
import emailprocessor.bing as bing
import os


@click.group()
@click.pass_context
@click.option('--address', '-a', default=None)
@click.option('--port', '-p', default=None, type=int)
@click.option('--debug/--no-debug', default=False)
@click.option('--timeout', default=None, type=int)
@click.option('--username', default=None, type=str)
def emailprocessor(ctx, address, port, debug, timeout, username):
    """Simple SMTP server for processing emails"""
    if username is None:
        username = os.environ.get('EMAILPROCESSOR_USERNAME')
    if port is None:
        port = int(os.environ.get('EMAILPROCESSOR_PORT'))
    if address is None:
        address = os.environ.get('EMAILPROCESSOR_ADDRESS')
    ctx.obj = {'address': address, 'port': port, 'debug': debug,
               'timeout': timeout, 'username': username}


@emailprocessor.command()
@click.pass_context
def email_summary(ctx):
    """Prints a summary of the email"""
    with basic.PrintSummarySMTPServer(
            (ctx.obj['address'], ctx.obj['port']),
            debug=ctx.obj['debug'],
            timeout=ctx.obj['timeout'],
            username=ctx.obj['username']) as server:
        server.run()


@emailprocessor.command()
@click.pass_context
@click.option('--directory', default='/var/email-processor')
def save_attachments(ctx, directory):
    """Saves email attachments"""
    server = basic.SaveAttachmentsSMTPServer(addr=(ctx.obj['address'],
                                              ctx.obj['port']),
                                             debug=ctx.obj['debug'],
                                             timeout=ctx.obj['timeout'],
                                             username=ctx.obj['username'],
                                             directory=directory)
    server.run()

@emailprocessor.command()
@click.pass_context
@click.option('--prefix',
              default=os.environ.get('EMAILPROCESSOR_BING_TO_S3_PREFIX', ''))
@click.option('--bucket',
              default=os.environ.get('EMAILPROCESSOR_BING_TO_S3_BUCKET'))
def bing_to_s3(ctx, prefix, bucket):
    """Moves Bing reports to S3"""
    server = bing.BingReportsToS3SMTPServer(addr=(ctx.obj['address'],
                                                  ctx.obj['port']),
                                            debug=ctx.obj['debug'],
                                            timeout=ctx.obj['timeout'],
                                            username=ctx.obj['username'],
                                            prefix=prefix,
                                            bucket=bucket)
    server.run()


if __name__ == '__main__':
    emailprocessor()
