import os
from unittest import mock

from django.test import TestCase
from rest_framework.test import APIClient

from movies_db.settings import BASE_DIR
from movies_api import models


class TestMoviesApi(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.example_response = mock.MagicMock()

        with open(os.path.join(BASE_DIR, 'business_logic', 'tests', 'example_response.json')) as f:
            # mock Response object from requests module
            setattr(self.example_response, 'text', f.read())

    @mock.patch('requests.get')
    def test_movie_fetch(self, request_get_mock):
        request_get_mock.return_value = self.example_response
        response = self.client.post('/movies/', {'title': 'test'}, format='json')
        self.assertTrue('id' in response.data)
        id = response.data['id']
        self.assertTrue(models.Movie.objects.filter(id=id).exists())

    @mock.patch('requests.get')
    def test_request_with_no_title(self, request_get_mock):
        request_get_mock.return_value = self.example_response
        response = self.client.post('/movies/', {'name': 'test'}, format='json')
        self.assertNotEqual(response.status_code, 200)

        # check that nothing has been saved to the database
        self.assertFalse(models.Movie.objects.exists())
