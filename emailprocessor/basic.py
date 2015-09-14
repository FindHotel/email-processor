#!/usr/bin/env python
# -*- coding: utf-8 -*-


from emailprocessor import EmailProcessor
from emailprocessor.utils import _print
from datetime import datetime
import email.parser
import os
import abc
import uuid


class PrintSummary(EmailProcessor):
    def process(self, peer, mailfrom, rcpttos, data, **params):
        """Prints summary stats of the email"""
        _print("Receiving message from: {}".format(peer))
        _print("Message addressed from: {}".format(mailfrom))
        _print("Message addressed to  : {}".format(rcpttos))
        _print("Message length        : {}".format(len(data)))


    @property
    def name(self):
        return 'print_email_summary'


class ProcessAttachments(EmailProcessor, metaclass=abc.ABCMeta):
    def process(self, peer, mailfrom, rcpttos, data, **params):
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
            self.process_attachment(part.get_payload(decode=True), filename,
                **params)

    @abc.abstractmethod
    def process_attachment(self, payload, filename, **params):
        """To be implemented by final classes"""
        pass


class SaveAttachments(ProcessAttachments):
    def __init__(self, directory=None, **kwargs):
        super().__init__(**kwargs)
        self.directory = directory

    def process_attachment(self, payload, filename, **params):
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)

        target_file = os.path.join(self.directory, filename)
        with open(target_file, 'wb') as fp:
            fp.write(payload)
        _print("Saved {}".format(target_file))

    @property
    def name(self):
        return 'save_email_attachments'

