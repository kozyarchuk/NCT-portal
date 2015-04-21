import unittest
from application import application as app

class TestApplication(unittest.TestCase):

    def test_index_route(self):
        app.debug = True
        c = app.test_client()

        rv = c.get('/')
        assert "NCT PORTAL" in rv.data.decode("utf-8")

        rv = c.get('/index.html')
        assert "NCT PORTAL" in rv.data.decode("utf-8")

    def test_static_route(self):
        app.debug = True
        c = app.test_client()

        rv = c.get('static/css/animate.css')

        self.assertEquals(200,  rv.status_code)