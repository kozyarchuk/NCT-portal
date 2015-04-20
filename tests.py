import unittest
from application import application as app

class TestApplication(unittest.TestCase):

    def test_index_route(self):
        app.debug = True
        c = app.test_client()

        rv = c.get('/')
        assert "Hello" in rv.data