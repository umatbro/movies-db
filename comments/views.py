from typing import Any
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters import rest_framework as dj_filters

from comments import models, serializers, filters
import business_logic as bl


class CommentView(ListCreateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.CommentFilter

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        movie_id = request.data.get('movie_id', None)
        comment_body = request.data.get('body', None)
        comment = bl.add_comment(movie_id, comment_body)
        return Response(serializers.CommentSerializer(comment).data)
