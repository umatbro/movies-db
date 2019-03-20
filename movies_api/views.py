from typing import Any
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters import rest_framework as dj_filters

import business_logic as bl
from movies_api import serializers, models, filters


class MovieView(ListCreateAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.MovieFilter

    def post(self, request: Request, *args: Any, **kwargs: Any):
        title = request.data.get('title', None)
        movie = bl.fetch_movie_info(title)
        movie_s = serializers.MovieSerializer(movie)
        return Response(movie_s.data)


class TopMoviesView(ListAPIView):
    serializer_class = serializers.MovieRankingSerializer

    def get_queryset(self):
        date_from = bl.utils.parse_date(self.request.query_params.get('date_from'))
        date_until = bl.utils.parse_date(self.request.query_params.get('date_until'))

        return bl.get_ranking(date_from, date_until)
