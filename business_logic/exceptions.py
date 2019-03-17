from django.utils.deprecation import MiddlewareMixin
from typing import List
from rest_framework import serializers
from django.http import JsonResponse


class BusinessLogicException(Exception):
    def __init__(self, message: str = '', errors: List = None, code: int = 500):
        self.message = message
        self.errors = errors
        if not errors:
            self.errors = []
        self.code = code


class BusinessLogicExceptionSerializer(serializers.Serializer):
    message = serializers.CharField()
    code = serializers.IntegerField()
    errors = serializers.ListField()


class BusinessLogicExceptionHandlerMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, BusinessLogicException):
            serializer = BusinessLogicExceptionSerializer(exception)
            return JsonResponse(serializer.data, status=exception.code)
