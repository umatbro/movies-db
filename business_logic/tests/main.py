import os
import json
from django.test import TestCase
from unittest import mock
import datetime as dt

import business_logic as bl
from movies_api import models
from movies_db.settings import OMDB_API_KEY


class TestMovie(TestCase):
    def setUp(self):
        self.example_response = mock.MagicMock()

        with open(os.path.join(os.path.dirname(__file__), 'example_response.json')) as f:
            # mock Response object from requests module
            setattr(self.example_response, 'text', f.read())

        self.response_with_error = mock.MagicMock()
        self.response_with_error.text = json.dumps({
            'Response': False,
            'Error': 'Movie not found.',
        })

        self.response_with_missing_fields = mock.MagicMock()
        with open(os.path.join(os.path.dirname(__file__), 'response_with_missing_fields.json')) as f:
            self.response_with_missing_fields.text = f.read()

    @mock.patch('requests.get')
    def test_valid_request_to_external_api_was_made(self, request_get_mock):
        """
        Check whether valid request was sent to the external API.
        """
        request_get_mock.return_value = self.example_response
        bl.fetch_movie_info('avengers')
        request_get_mock.assert_called_with(f'{bl.API_HOST}?t=avengers&apikey={OMDB_API_KEY}')

    @mock.patch('requests.get')
    def test_fetch_movie(self, request_get_mock):
        """
        Test if movie was fetched  and saved to database.
        """
        request_get_mock.return_value = self.example_response
        movie = bl.fetch_movie_info('avengers')
        request_get_mock.assert_called()

        self.assertEqual(movie.title, 'The Avengers')
        self.assertEqual(movie.release_date, dt.date(2012, 5, 4))
        self.assertEqual(movie.cover, 'https://example_host.com/pic.jpg/')
        self.assertEqual(movie.duration, 143)
        self.assertEqual(movie.director, 'Joss Whedon')
        self.assertEqual(movie.website, 'http://marvel.com/avengers_movie')

        # test if movie is in database
        self.assertTrue(models.Movie.objects.filter(id=movie.pk).exists())

    @mock.patch('requests.get')
    def test_error_response_from_server(self, request_get_mock):
        """
        Case when there was an error returned by external API.
        """
        request_get_mock.return_value = self.response_with_error
        with self.assertRaisesMessage(bl.exceptions.BusinessLogicException, 'Movie not found.'):
            bl.fetch_movie_info('there is no movie with this name')

    @mock.patch('requests.get')
    def test_response_with_missing_data(self, request_get_mock):
        """
        Case when we receive response with some missing fields.
        """
        request_get_mock.return_value = self.response_with_missing_fields
        movie = bl.fetch_movie_info('hipster movie')

        self.assertEqual(movie.title, 'Some hipster movie')
        self.assertEqual(movie.release_date, None)
        self.assertEqual(movie.cover, None)
        self.assertEqual(movie.duration, None)
        self.assertEqual(movie.director, None)
        self.assertEqual(movie.website, None)


class TestComments(TestCase):
    def setUp(self):
        self.movie = models.Movie.objects.create(title='Test')

    def test_add_comment(self):
        bl.add_comment(self.movie.id, 'this is a test comment')

        # check if comment exists in database
        self.assertTrue(self.movie.comment_set.all().exists())
        self.assertEquals(self.movie.comment_set.first().body, 'this is a test comment')

    def test_do_not_add_comment_if_movie_id_does_not_exist(self):
        non_existing_id = self.movie.id + 1
        with self.assertRaisesMessage(bl.exceptions.BusinessLogicException, 'does not exist'):
            bl.add_comment(non_existing_id, 'this won\'t work anyway')
