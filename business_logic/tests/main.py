import os
import json
from typing import List
from django.test import TestCase
from unittest import mock
import datetime as dt

import business_logic as bl
from movies_api import models
from movies_db.settings import OMDB_API_KEY
from comments.models import Comment


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

    def test_do_not_add_comment_with_empty_body(self):
        with self.assertRaisesMessage(bl.exceptions.BusinessLogicException, 'cannot be empty'):
            bl.add_comment(self.movie.id, '')

    def test_movie_id_is_none(self):
        with self.assertRaises(bl.exceptions.BusinessLogicException):
            bl.add_comment(None, 'test')


class TestTopMovies(TestCase):
    def setUp(self):
        self.mov1 = models.Movie.objects.create(title='mov1')
        self.mov2 = models.Movie.objects.create(title='mov2')
        self.mov3 = models.Movie.objects.create(title='mov3')
        self.mov4 = models.Movie.objects.create(title='mov4')
        self.mov5 = models.Movie.objects.create(title='mov5')
        self.mov_out_of_range = models.Movie.objects.create(title='mov')

        def create_comments_for_movie(movie: models.Movie, num_of_comments: int, dates: List[dt.date] = None):
            """
            Create comments for given movie.

            :param movie:
            :param num_of_comments:
            :param dates: a list containing dates to assign to comments. Should be the length of num_of_comments
            """
            if dates is None:
                dates = [dt.date(2010, 1, 1)] * num_of_comments
            for i, date in zip(range(num_of_comments), dates):
                Comment.objects.create(movie=movie, body=f'comment {i}', publish_date=date)

        create_comments_for_movie(self.mov_out_of_range, 2, [dt.date(1970, 1, 1), dt.date(1970, 1, 2)])
        create_comments_for_movie(self.mov1, 3)
        create_comments_for_movie(self.mov2, 4)
        create_comments_for_movie(self.mov3, 2)
        create_comments_for_movie(self.mov4, 3)
        create_comments_for_movie(self.mov5, 5, [dt.date(1970, 1, 1)] + [dt.date(2010, 1, 1)] * 3 + [dt.date(2020, 1, 1)])

    def test_fetch_ranking(self):
        ranking = bl.get_ranking(dt.date(2000, 1, 1), dt.date(2011, 1, 1))

        # compare number of comments
        self.assertListEqual(
            [4, 3, 3, 3, 2, 0],
            [movie.total_comments for movie in ranking]
        )

        # compare rank
        self.assertListEqual(
            [1, 2, 2, 2, 3, 4],
            [movie.rank for movie in ranking]
        )

        # check if self.mov5 has rank 2 and 3 comments were taken into account
        mov5 = ranking.get(id=self.mov5.id)
        self.assertEqual(mov5.total_comments, 3)

    def test_edge_date_values(self):
        models.Movie.objects.all().delete()
        mov = models.Movie.objects.create(title='mov')
        edge_date_from = dt.date(2030, 1, 1)
        edge_date_until = dt.date(2031, 1, 1)
        min_timedelta = dt.timedelta(days=1)

        # create 6 comments, only 4 of them should be captured by given range
        Comment.objects.create(movie=mov, publish_date=edge_date_from - min_timedelta)
        Comment.objects.create(movie=mov, publish_date=edge_date_from)
        Comment.objects.create(movie=mov, publish_date=edge_date_from + min_timedelta)
        Comment.objects.create(movie=mov, publish_date=edge_date_until - min_timedelta)
        Comment.objects.create(movie=mov, publish_date=edge_date_until)
        Comment.objects.create(movie=mov, publish_date=edge_date_until + min_timedelta)

        ranking = bl.get_ranking(edge_date_from, edge_date_until)
        self.assertEqual(ranking.count(), 1)
        movie_from_ranking = ranking.first()
        self.assertEqual(movie_from_ranking.total_comments, 4)
