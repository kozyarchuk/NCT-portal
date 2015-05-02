import os
os.environ['SECRET_KEY'] = 'xxx'

import unittest
from domain.file_record import FileRecord
from testlib.test_s3 import BucketRecord, Bucket
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class TestFileRecord(unittest.TestCase):

    def test_file_record_display(self):
        br = BucketRecord(1)
        fr = FileRecord(br)
        self.assertEquals("Some Name1",fr.name)
        self.assertEquals(123,fr.size)
        self.assertEquals('2015-04-01T15:16:55Z',fr.upload_time)
        self.assertEquals('April 01, 2015 03:16PM',fr.formatted_upload_time)

    def test_get_latest(self):
        records = FileRecord.get_latest(Bucket(5),count = 2)
        self.assertEquals(2, len(records))
        r1, r2 = records
        self.assertTrue(r1.upload_time > r2.upload_time)

    def test_upload_file_when_no_trade_file(self):
        msg, err = FileRecord.upload_file(Bucket(1),None)
        self.assertEquals("File is missing", msg)
        self.assertEquals("error", err)

    def test_upload_file_illigal_file_name(self):
        class FileMsg:
            filename = 'xxxx.doc'
        msg, err = FileRecord.upload_file(Bucket(1),FileMsg())
        self.assertTrue("Unsupported extension .doc" in msg)
        self.assertEquals("error", err)

    def test_upload_file_loads_file_to_bucket(self):
        class FileMsg:
            filename = 'xxxx.csv'
            stream = StringIO()
        FileMsg.stream.write('file content')
        FileMsg.stream.seek(0)
        bucket = Bucket(1)
        msg, err = FileRecord.upload_file(bucket,FileMsg())
        self.assertEquals("File Saved", msg)
        self.assertEquals("info", err)
        self.assertEquals("file content", bucket.key.data)

if __name__ == '__main__':
    unittest.main()
