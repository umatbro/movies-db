import json
from io import BytesIO

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


from movies_api.models import Movie


class TestCommentsApi(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(title='Test')
        self.client = APIClient()

    def test_add_comment(self):
        response = self.client.post(reverse('comments'), {'movie_id': self.movie.id, 'body': 'comment'})
        # check response contents
        self.assertEqual(response.data['movie'], self.movie.id)
        self.assertEqual(response.data['body'], 'comment')

        # check if model has been saved to the database
        self.assertEqual(self.movie.comment_set.count(), 1)
        self.assertEqual(self.movie.comment_set.first().body, 'comment')

    def test_fail_to_add_comment_with_no_movie_id_provided_in_request_body(self):
        response = self.client.post(reverse('comments'), {'body': 'comment'})
        self.assertEqual(response.status_code, 400)
        res_body = json.load(BytesIO(response.content))
        self.assertEqual(res_body['message'], 'Provide movie_id in request body.')
