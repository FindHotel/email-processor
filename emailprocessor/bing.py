from emailprocessor.basic import ProcessAttachmentsSMTPServer
from emailprocessor.utils import _print
import uuid
import sh
import os
from datetime import datetime


class BingReportsToS3SMTPServer(ProcessAttachmentsSMTPServer):
    def __init__(self, prefix=None, **kwargs):
        super().__init__(**kwargs)
        self.prefix = prefix

    @property
    def s3key(self):
        now = datetime.now()
        filename = "{year}-{month}-{day}.tsv.zip".format(
            year=now.year, month=now.month, day=now.day)
        return os.path.join(self.prefix, filename)

    def _process_attachment(self, payload, filename):
        target_file = os.path.join('/tmp', str(uuid.uuid4()))
        with open(target_file, 'wb') as fp:
            fp.write(payload)
        _print("Saved {}".format(target_file))
        aws = sh.aws.bake()
        aws('s3', 'cp', target_file, self.s3key)
        _print("Produced {}".format(self.s3key))
        os.remove(target_file)
        _print("Deleted {}".format(target_file))
