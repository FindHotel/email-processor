#!/usr/bin/env python
# -*- coding: utf-8 -*-


from smtpd import SMTPServer
import contextlib
import emailprocessor.config as config
import asyncore


class BaseSMTPServer(SMTPServer, contextlib.ContextDecorator):
    """Some basic enhancements on top of the vanilla SMTPServer class"""
    def __init__(self, addr=(config.address, config.port), remote_addr=None,
                 debug=False, timeout=None, **kwargs):
        super().__init__(addr, remote_addr, **kwargs)
        self.debug = debug
        self.timeout = timeout
        print("Created SMTP server <{}:{}>".format(addr[0], addr[1]))

    def run(self):
        """Start listening for incoming emails"""
        print("Listening for incoming emails on {}:{} ...".format(*self.addr))
        if not self.timeout:
            asyncore.loop()
        else:
            asyncore.loop(timeout=1, count=self.timeout)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.socket.close()
