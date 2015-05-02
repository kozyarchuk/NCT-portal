from boto.sqs.message import Message
import boto


class S3:
    BUCKET = 'nct-data'
    _conn = None

    def get_file_upload_bucket(self):
        return  self.conn.get_bucket(self.BUCKET)

    @property
    def conn(self):
        if not self._conn:
            self._conn = boto.connect_s3()
        return self._conn
#     @property
#     def sqs(self):
#         if not self._sqs:
#             self._sqs = boto.sqs.connect_to_region("us-east-1")
#         return self._sqs

gw = S3()