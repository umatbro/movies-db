from typing import Any
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request

from comments import models, serializers
import business_logic as bl


class CommentView(ListCreateAPIView):
    queryset = models.Comment
    serializer_class = serializers.CommentSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        movie_id = request.data.get('movie_id', None)
        comment_body = request.data.get('body', None)
        comment = bl.add_comment(movie_id, comment_body)
        return Response(serializers.CommentSerializer(comment).data)
