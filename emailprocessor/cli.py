#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Command line interface"""

from __future__ import print_function

import click
import emailprocessor.basic as basic
import emailprocessor.bing as bing
from emailprocessor import EmailServer
import os
import uuid


@click.group()
@click.pass_context
@click.option('--address', '-a', default=None)
@click.option('--port', '-p', default=None, type=int)
@click.option('--debug/--no-debug', default=False)
@click.option('--timeout', default=None, type=int)
@click.option('--certfile', default=None, type=str)
@click.option('--certkey', default=None, type=str)
@click.option('--username', default=None, type=str)
def emailprocessor(ctx, address, port, debug, timeout, username, certkey,
                   certfile):
    """Simple SMTP server for processing emails"""
    username = _resolve_username(username)
    if address is None:
        address = os.environ.get('EMAILPROCESSOR_ADDRESS')
    if port is None:
        port = int(os.environ.get('EMAILPROCESSOR_PORT'))
    if certkey is None:
        certkey = os.environ.get('EMAILPROCESSOR_CERTKEY')
    if certfile is None:
        certfile = os.environ.get('EMAILPROCESSOR_CERTFILE')

    server = EmailServer(addr=(address, port), debug=debug, timeout=timeout,
                         certfile=certfile, certkey=certkey)

    ctx.obj = {'server': server, 'username': username}


def _resolve_username(username):
    if username is None:
        username = os.environ.get('EMAILPROCESSOR_USERNAME')
        if username is None:
            username=str(uuid.uuid4())
    return username


@emailprocessor.command()
@click.pass_context
def email_summary(ctx):
    """Prints a summary of the email"""
    server = ctx.obj['server']
    server.register_processor(ctx.obj['username'], basic.PrintSummary())
    server.run()


@emailprocessor.command()
@click.pass_context
@click.option('--directory', default='/var/email-processor')
def save_attachments(ctx, directory):
    """Saves email attachments"""
    server = ctx.obj['server']
    server.register_processor(ctx.obj['username'],
                              basic.SaveAttachments(directory))
    server.run()


@emailprocessor.command()
@click.pass_context
@click.option('--prefix',
              default=os.environ.get('EMAILPROCESSOR_BING_TO_S3_PREFIX', ''))
@click.option('--bucket',
              default=os.environ.get('EMAILPROCESSOR_BING_TO_S3_BUCKET'))
def bing_to_s3(ctx, prefix, bucket):
    """Moves Bing reports to S3"""
    server = ctx.obj['server']
    processor = bing.BingReportsToS3(bucket=bucket, prefix=prefix)
    server.register_processor(ctx.obj['username'], processor)
    server.run()


if __name__ == '__main__':
    emailprocessor()
