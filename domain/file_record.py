import dateutil.parser
import time
import os
from werkzeug import secure_filename

class FileRecord:
    ALLOWED_EXTENSIONS = set(['.txt', '.csv', '.xls', '.xlsx','.dat'])

    def __init__(self, key):
        self.name = key.name
        self.size = key.size
        self.upload_time = key.last_modified

    def __cmp__(self, other):
        return cmp(self.upload_time, other.upload_time)

    def __lt__(self, other):
        return self.upload_time < other.upload_time

    @property
    def formatted_upload_time(self):
        d = dateutil.parser.parse(self.upload_time)
        return d.strftime("%B %d, %Y %I:%M%p")

    @classmethod
    def get_latest(cls, bucket, count = 20):
        ordered_list = sorted(bucket.list(), key=lambda k: k.last_modified)
        return sorted([ FileRecord(key) for key in ordered_list[0:count] ], reverse=True)

    @classmethod
    def upload_file(cls, bucket, trade_file):
        if trade_file:
            base_name, extension = os.path.splitext(secure_filename(trade_file.filename))
            if extension in cls.ALLOWED_EXTENSIONS:
                file_name = "%s.%s.%s" % (base_name, time.time(), extension)
                key = bucket.new_key(file_name)
                key.set_contents_from_string(trade_file.stream.read())
                return ("File Saved", 'info')
            else:
                return ("Unsupported extension %s. Only %s are supported" % (extension, cls.ALLOWED_EXTENSIONS), 'error')
        else:
            return("File is missing", 'error')
