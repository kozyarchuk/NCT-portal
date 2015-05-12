

class BucketRecord:
    def __init__(self, offset):
        self.name = 'Some Name%s' % offset
        self.size = 123
        self.last_modified = "2015-04-%02dT15:16:55Z" % offset


class Key:
    def __init__(self, name):
        self.name = name
        self.data = None
        self.metadata = {}

    def set_contents_from_string(self, data):
        self.data = data

    def set_metadata(self, name, value):
        self.metadata[name] = value
        
class Bucket:
    def __init__(self, size):
        self.size = size
        self.key = None

    def list(self):
        return [BucketRecord(i) for i in range(self.size,1,-1)]

    def new_key(self, file_name):
        self.key = Key(file_name)
        return self.key


class S3:
    def __init__(self):
        self.bucket = None

    def get_file_upload_bucket(self):
        self.bucket = Bucket(30)
        return self.bucket
