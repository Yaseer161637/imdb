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

    def test_dashboard_view(self):
        """
        Test the dashboard view.
        """
        response = self.client.get('/dashboard')
        self.assert200(response)
        self.assertIn(b'Dashboard', response.data)

    def test_upload_csv_view(self):
        """
        Test the CSV upload view.
        """
        # Login user
        with self.client:
            response = self.client.post('/login', data=dict(
                username='test_user',
                password='test_password'
            ), follow_redirects=True)
            self.assertIn(b'You were logged in.', response.data)

            # Upload CSV file
            with open('test.csv', 'rb') as f:
                response = self.client.post('/csv_upload', data=dict(
                    csv_file=(f, 'test.csv')
                ), follow_redirects=True)
                self.assertIn(b'Uploaded successfully.', response.data)

    def test_file_progress_view(self):
        """
        Test the file progress view.
        """
        # Login user
        with self.client:
            response = self.client.post('/login', data=dict(
                username='test_user',
                password='test_password'
            ), follow_redirects=True)
            self.assertIn(b'You were logged in.', response.data)

            # Add file progress entry
            file_progress = FileProgress(username='test_user', filepath='test.csv', added_count=10, status='Completed')
            file_progress.save()

            response = self.client.get('/file_progress')
            self.assert200(response)
            self.assertIn(b'File Progress', response.data)
            self.assertIn(b'test.csv', response.data)


if __name__ == '__main__':
    unittest.main()
