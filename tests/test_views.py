# tests/test_views.py
import os
import unittest

from flask_testing import TestCase
from pymongo import MongoClient

from imdb import app
from imdb.models import FileProgress


class TestMovieViews(TestCase):
    def create_app(self):
        """
        Create an instance of the Flask application with testing configuration.
        """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        """
        Set up test client for each test case.
        """
        self.client = self.app.test_client()

        # Mock database connection
        self.client.db = MongoClient(os.getenv('ENV_DB_URL'))


if __name__ == '__main__':
    unittest.main()
