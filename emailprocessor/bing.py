from emailprocessor.basic import ProcessAttachments
from emailprocessor.utils import _print, filename_from_string
from emailprocessor.exceptions import InitError
import uuid
import boto3
import os
import re
import io
import dateutil.parser as date_parser
from zipfile import ZipFile
from collections import namedtuple


BingHeader = namedtuple('BingReportHeader', "first_day last_day aggregation "
                        "filter rows account type version")


class BingReportsToS3(ProcessAttachments):
    def __init__(self, bucket=None, prefix='', **kwargs):
        super().__init__(**kwargs)
        if bucket is None:
            raise InitError("A bucket URI must be specified")
        self.bucket = bucket
        self.prefix = prefix
        self.__client = None

    @property
    def name(self):
        return 'bing_report_to_s3'

    def get_s3key(self, payload):
        """Produces a meaningful S3 key based on the report properties:
        reporting period, reporting account, etc"""
        with ZipFile(io.BytesIO(payload)) as myzip:
            # Should contain just one file: the report
            file = myzip.filelist[0]
            msg = "Processing {}, created on {}-{}-{} {}:{}:{}".format(
                file.filename, *file.date_time)
            _print(msg)
            with myzip.open(file.filename, 'r') as myfile:
                hdr = self._process_header(myfile)

        unknown_account = "unknown-{}".format(uuid.uuid4())
        account = filename_from_string(hdr.account or unknown_account)
        return os.path.join(self.prefix, hdr.type.lower(),
                            str(hdr.first_day.year),
                            str(hdr.first_day.month), str(hdr.first_day.day),
                            account + '.tsv.zip')

    @staticmethod
    def _process_report_time(text):
        first_day, last_day = None, None
        match = re.match('"Report Time: ([\d/]+),?([\d/]*)".*', text)
        if match:
            first_day, last_day = match.groups()
            first_day = date_parser.parse(first_day)
            if len(last_day) == 0:
                # Reporting period is one day
                last_day = first_day
            else:
                last_day = date_parser.parsee(last_day)
        return (first_day, last_day)

    @staticmethod
    def _process_report_name(text):
        account, reptype, repversion = [None]*3
        match = re.match('"Report Name: (.+)".*', text)
        if match:
            name = match.groups()[0].lower()
            account, reptype, repversion = name.split('-')
        return (account, reptype, repversion)

    def _process_header(self, myfile):
        # Look for the "Report Time" row until we find a blank line
        first_day, last_day, aggr, filterstr, nbrows, account, reptype, \
            repversion = [None]*8
        for row in myfile:
            # Bing uses UTF-8 with BOM encoding
            text = row.decode('utf-8-sig')
            if account is None:
                account, reptype, repversion = self._process_report_name(text)
            if first_day is None:
                first_day, last_day = self._process_report_time(text)
            match = re.match('"Report Aggregation: (\w+)".+', text)
            if match:
                aggr = match.groups()[0].lower()
            match = re.match('"Report Filter: " (.+)".+', text)
            if match:
                filterstr = match.groups()[0]
            match = re.match('"Rows: (\d+)".+', text)
            if match:
                nbrows = int(match.groups()[0])

        return BingHeader(first_day, last_day, aggr, filterstr, nbrows,
                          account, reptype, repversion)

    @property
    def client(self):
        """Caches the boto3 S3 client"""
        if self.__client is None:
            self.__client = boto3.client('s3')
        return self.__client

    def process_attachment(self, payload, filename):
        s3key = self.get_s3key(payload)
        self.client.put_object(ACL='private', Bucket=self.bucket, Body=payload,
                               Key=s3key)
        _print("Produced {}".format(s3key))
