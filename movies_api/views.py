from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

import business_logic as bl
from movies_api import serializers, models


class MovieView(APIView):
    def post(self, request: Request) -> Response:
        title = request.data.get('title', None)
        movie = bl.fetch_movie_info(title)
        movie_s = serializers.MovieSerializer(movie)
        return Response(movie_s.data)

    def get(self, request: Request) -> Response:
        movies = models.Movie.objects.all()
        serializer = serializers.MovieSerializer(movies, many=True)
        return Response(serializer.data)
