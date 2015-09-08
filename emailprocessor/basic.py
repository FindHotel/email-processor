#!/usr/bin/env python
# -*- coding: utf-8 -*-


from emailprocessor.common import BaseSMTPServer
from emailprocessor.utils import _print
from datetime import datetime
import email.parser
import os
import abc
import uuid


class PrintSummarySMTPServer(BaseSMTPServer):
    def _process(self, peer, mailfrom, rcpttos, data):
        """Prints summary stats of the email"""
        _print("Receiving message from: {}".format(peer))
        _print("Message addressed from: {}".format(mailfrom))
        _print("Message addressed to  : {}".format(rcpttos))
        _print("Message length        : {}".format(len(data)))


class ProcessAttachmentsSMTPServer(BaseSMTPServer, metaclass=abc.ABCMeta):
    def _process(self, peer, mailfrom, rcpttos, data):
        """Saves email attachments in the specified directory"""
        parser = email.parser.Parser()
        msgobj = parser.parsestr(data)
        for part in msgobj.walk():
            if part.is_multipart():
                # multipart are just containers
                continue
            filename = part.get_filename()
            if not filename:
                # Not an attachment
                continue
            self._process_attachment(part.get_payload(decode=True), filename)

    @abc.abstractmethod
    def _process_attachment(self, payload, filename):
        """To be implemented by final classes"""
        pass


class SaveAttachmentsSMTPServer(ProcessAttachmentsSMTPServer):
    def __init__(self, directory=None, **kwargs):
        super().__init__(**kwargs)
        self.directory = directory

    def _process_attachment(self, payload, filename):
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)

        target_file = os.path.join(self.directory, filename)
        with open(target_file, 'wb') as fp:
            fp.write(payload)
        _print("Saved {}".format(target_file))
