import re
import json
import requests
import logging
from urllib import parse
from dateutil.parser import parse as parse_date

from django.core.exceptions import ValidationError
from rest_framework import status as s

from movies_api import models
from comments.models import Comment
from movies_db.settings import OMDB_API_KEY
from business_logic import exceptions, utils


API_HOST = 'http://www.omdbapi.com/'

logger = logging.getLogger(__name__)


def fetch_movie_info(title: str, save_to_db: bool = True) -> models.Movie:
    """
    Fetch movie details from external API and save it to database.

    :param title: title of the movie to save.
    :param save_to_db: this should be set to False if fetched object should not be saved to database.
    :return: movie that was saved to database
    :raises: BusinessLogicException if no movie was saved to database.
    """
    if not title:
        raise exceptions.BusinessLogicException('Please provide title movie', code=s.HTTP_400_BAD_REQUEST)

    query = parse.urlencode({'t': title, 'apikey': OMDB_API_KEY})
    request_addr = f'{API_HOST}?{query}'
    logger.info(f'Fetching resources from: {request_addr}')
    res = requests.get(request_addr)
    movie_dict = json.loads(res.text)

    if 'Error' in movie_dict:
        logger.error(f'Information about movie {title} could not be fetched (response: {movie_dict["Error"]})')
        raise exceptions.BusinessLogicException(movie_dict['Error'])

    f = utils.read_field

    release_date = f(movie_dict, 'Released')
    duration = f(movie_dict, 'Runtime')

    movie = models.Movie(
        title=f(movie_dict, 'Title'),
        cover=f(movie_dict, 'Poster'),
        release_date=parse_date(release_date) if release_date else None,
        duration=int(re.sub(r'[^0-9]', '', duration)) if duration else None,
        director=f(movie_dict, 'Director'),
        website=f(movie_dict, 'Website'),
    )

    if not save_to_db:
        return movie

    try:
        movie.save()
        movie.refresh_from_db()
        logger.info(f'Movie {movie.title} (id: {movie.pk}) saved to database.')
    except ValidationError as e:
        logger.exception(e)
        raise exceptions.BusinessLogicException(e)

    return movie


def add_comment(movie_id: int, comment_body: str) -> Comment:
    """
    Add comment to desired movie.

    :param movie_id:
    :param comment_body:
    :return: comment instance that was created
    :raises BusinessLogicException: when invalid movie id was provided
    """
    if not movie_id:
        raise exceptions.BusinessLogicException('Provide movie_id in request body.', code=s.HTTP_400_BAD_REQUEST)
    if not comment_body:
        raise exceptions.BusinessLogicException('Comment cannot be empty.', code=s.HTTP_400_BAD_REQUEST)
    try:
        movie = models.Movie.objects.get(id=movie_id)
    except models.Movie.DoesNotExist:
        raise exceptions.BusinessLogicException(f'Movie with id {movie_id} does not exist.', code=s.HTTP_404_NOT_FOUND)

    comment = Comment.objects.create(movie=movie, body=comment_body)
    logger.info(f'Comment id:{comment.id} for movie ({movie.id}) has been saved.')
    return comment
