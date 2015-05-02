import os
os.environ['SECRET_KEY'] = 'xxx'
import unittest
from application import application as app
from gateway import s3
from testlib import test_s3
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
    
class TestApplication(unittest.TestCase):

    def setUp(self):
        self.s3 = test_s3.S3()
        s3.gw = self.s3

        app.debug = True
        self.c = app.test_client()

    def test_index_route(self):

        rv = self.c.get('/')
        assert "NCT PORTAL" in rv.data.decode("utf-8")

        rv = self.c.get('/index.html')
        assert "NCT PORTAL" in rv.data.decode("utf-8")

    def test_static_route(self):

        rv = self.c.get('static/css/animate.css')

        self.assertEquals(200,  rv.status_code)

    def test_files_route(self):

        rv = self.c.get('/files.html')
        assert "Trade Files" in rv.data.decode("utf-8")

    def test_files_route(self):

        rv = self.c.post('/files.html',
                         data=dict(trade_file=(StringIO('fake file'), 'file.csv')) )
        assert "files.html" in rv.data.decode("utf-8")
