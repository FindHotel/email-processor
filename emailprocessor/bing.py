from emailprocessor.basic import ProcessAttachmentsSMTPServer
from emailprocessor.utils import _print
from emailprocessor.exceptions import InitError
import uuid
import boto3
import os
import zipfile
from datetime import datetime


class BingReportsToS3SMTPServer(ProcessAttachmentsSMTPServer):
    def __init__(self, bucket=None, prefix='', **kwargs):
        super().__init__(**kwargs)
        if bucket is None:
            raise InitError("A bucket URI must be specified")
        self.bucket = bucket
        self.prefix = prefix
        self.__client = None

    def get_s3key(self, payload):
        """Produces a meaningful S3 key based on the report properties: 
        reporting period, reporting account, etc"""
        # for now, a dummy method
        now = datetime.now()
        filename = "{year}-{month}-{day}.tsv.zip".format(
            year=now.year, month=now.month, day=now.day)
        return os.path.join(self.prefix, filename)

    @property
    def client(self):
        """Caches the boto3 S3 client"""
        if self.__client is None:
            self.__client = boto3.client('s3')
        return self.__client

    def _process_attachment(self, payload, filename):
        s3key = self.get_s3key(payload)
        self.client.put_object(ACL='private', Bucket=self.bucket, Body=payload,
                               Key=s3key)
        _print("Produced {}".format(s3key))
