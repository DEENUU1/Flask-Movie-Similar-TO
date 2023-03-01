import pytest
from requests import Response
from unittest import mock
from similar_movies.search_movie import SearchMovie


@pytest.fixture
def mock_search_movie():
    return SearchMovie("Ant man and the wasp")


@pytest.fixture
def movie_search():
    return SearchMovie()


def test_create_query(mock_search_movie):
    assert mock_search_movie.create_query() == "ant-man-and-the-wasp"


def mocked_requests_get(*args):
    if args[0] == f"https://api.themoviedb.org/3/search/movie?api_key=fakeapikey&query=the-transporter":
        return Response().json(status_code=200)


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_return_movie_id(mock_get, movie_search):
    movie_search.query = "The Transporter"
    assert movie_search.return_movie_id == "4108"
