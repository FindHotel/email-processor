from emailprocessor.common import BaseSMTPServer


class PrintSummarySMTPServer(BaseSMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        print("Receiving message from: {}".format(peer))
        print("Message addressed from: {}".format(mailfrom))
        print("Message addressed to  : {}".format(rcpttos))
        print("Message length        :".format(len(data)))
