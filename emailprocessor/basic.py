from emailprocessor.common import BaseSMTPServer
import email.parser


class PrintSummarySMTPServer(BaseSMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        """Prints summary stats of the email"""
        print("Receiving message from: {}".format(peer))
        print("Message addressed from: {}".format(mailfrom))
        print("Message addressed to  : {}".format(rcpttos))
        print("Message length        : {}".format(len(data)))


class SaveAttachmentsSMTPServer(BaseSMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        """Saves email attachments in the specified directory"""
        parser = email.parser.Parser()
        msgobj = parser.parsestr(data)
        for part in msgobj.walk():
            attachment = self.email_parse_attachment(part)
            print(attachment)
