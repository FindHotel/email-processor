# -*- coding: utf-8 -*-
"""A simple SMTP server that receives and processes emails"""

from emailprocessor import metadata
from smtpd import SMTPServer
import contextlib
from emailprocessor.utils import _print
import asyncore
import uuid
import abc
from collections import defaultdict


__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright


class EmailProcessor(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def name(self):
        pass

    @abc.abstractproperty
    def process(self):
        pass


class EmailServer(SMTPServer, contextlib.ContextDecorator,
                     metaclass=abc.ABCMeta):
    """Some basic enhancements on top of the vanilla SMTPServer class"""
    def __init__(self, addr=None, remote_addr=None,  debug=False, timeout=None,
                 **kwargs):
        super().__init__(addr, remote_addr)
        self.debug = debug
        self.timeout = timeout
        self.processors = defaultdict(lambda: {})
        _print("Created SMTP server <{}:{}>".format(addr[0], addr[1]))

    def process_message(self, peer, mailfrom, rcpttos, data):
        """Some generic processing common to all server"""
        recipient = rcpttos[0].split('@')[0]
        _print("Receiving email from {} ({})".format(mailfrom, peer))
        username, params = self._process_recipient(recipient)
        if username in self.processors:
            _print("Processing ...")
            for proc in self.processors[username].values():
                _print("Running {} processor ...".format(proc.name))
                proc.process(peer, mailfrom, rcpttos, data, **params)
            _print("Done!")
        else:
            _print("No processors registered for {}".format(username))

    @staticmethod
    def _process_recipient(recipient):
        """The recipient is used for authentication and to pass parameters 
        to the processor"""
        username, *params = recipient.split('.')
        paramdict = {}
        for param in params:
            k, v = param.split('-')
            paramdict[k] = v

        return username, paramdict

    def register_processor(self, username, *processors):
        """Registers one ore more processor with a username"""
        for proc in processors:
            _print("Registered {} on {}".format(proc.name, username))
            self.processors[username][proc.name] = proc

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
