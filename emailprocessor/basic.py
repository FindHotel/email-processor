#!/usr/bin/env python
# -*- coding: utf-8 -*-


from emailprocessor.common import BaseSMTPServer
import email.parser
import os


class PrintSummarySMTPServer(BaseSMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        """Prints summary stats of the email"""
        print("Receiving message from: {}".format(peer))
        print("Message addressed from: {}".format(mailfrom))
        print("Message addressed to  : {}".format(rcpttos))
        print("Message length        : {}".format(len(data)))


class SaveAttachmentsSMTPServer(BaseSMTPServer):
    def __init__(self, directory=None, **kwargs):
        super().__init__(**kwargs)
        self.directory = directory

    def process_message(self, peer, mailfrom, rcpttos, data):
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
            if not os.path.isdir(self.directory):
                os.makedirs(self.directory)
            # We should sanitize the filename: TO DO!
            target_file = os.path.join(self.directory, filename)
            with open(target_file, 'wb') as fp:
                fp.write(part.get_payload(decode=True))
            print("==> Saved {}".format(target_file))
