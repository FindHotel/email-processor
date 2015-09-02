#!/usr/bin/env python
# -*- coding: utf-8 -*-


from smtpd import SMTPServer
import asyncore


class BaseSMTPServer(SMTPServer):
    """Some basic enhancements on top of the vanilla SMTPServer class"""
    def run(self):
        """Start listening for incoming emails"""
        print("Listening for incoming emails on {}:{} ...".format(*self.addr))
        asyncore.loop()
