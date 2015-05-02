import unittest
from application import application as app
import  os

class TestApplication(unittest.TestCase):

    def setUp(self):
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


    # def test_files_route(self):
    #
    #     rv = self.c.get('/files.html')
    #     print (rv.data)
    #     assert "Upload File" in rv.data.decode("utf-8")

    # def test_files_route(self):
    #
    #     rv = self.c.post('/files.html')
    #     assert "Message Sent" in rv.data.decode("utf-8")
