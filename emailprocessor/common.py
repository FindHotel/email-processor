#!/usr/bin/env python
# -*- coding: utf-8 -*-


from smtpd import SMTPServer
import contextlib
import emailprocessor.config as config
from emailprocessor.utils import _print
import asyncore
import uuid
import abc


class BaseSMTPServer(SMTPServer, contextlib.ContextDecorator,
                     metaclass=abc.ABCMeta):
    """Some basic enhancements on top of the vanilla SMTPServer class"""
    def __init__(self, addr=(config.address, config.port), remote_addr=None,
                 debug=False, timeout=None, username=None, **kwargs):
        super().__init__(addr, remote_addr)
        self.debug = debug
        self.timeout = timeout
        if username is None:
            # Use a randomly generated inboxname
            username=str(uuid.uuid4())
        self.username = username
        _print("Created SMTP server <{}:{}>".format(addr[0], addr[1]))
        _print("Processing emails sent to {}".format(username))

    def process_message(self, peer, mailfrom, rcpttos, data):
        """Some generic processing common to all server"""
        recipient = rcpttos[0].split('@')[0]
        _print("Receiving email from {} ({})".format(mailfrom, peer))
        if recipient == self.username:
            _print("Processing ...")
            self._process(peer, mailfrom, rcpttos, data)
        else:
            _print("Ignoring email sent to {}".format(recipient))

    @abc.abstractmethod
    def _process(peer, mailfrom, rcpttos, data):
        """To be implemented by final SMTP server classes"""
        pass

    def run(self):
        """Start listening for incoming emails"""
        _print("Listening for incoming emails on {}:{} ...".format(*self.addr))
        if not self.timeout:
            asyncore.loop()
        else:
            asyncore.loop(timeout=1, count=self.timeout)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.socket.close()
