from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

import business_logic as bl
from movies_api import serializers


class MovieView(APIView):
    def post(self, request: Request) -> Response:
        title = request.data.get('title', None)
        movie = bl.fetch_movie_info(title)
        movie_s = serializers.MovieSerializer(movie)
        return Response(movie_s.data)
