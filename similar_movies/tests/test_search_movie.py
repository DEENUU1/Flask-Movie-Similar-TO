import pytest
from requests import Response
from unittest import mock
from similar_movies.search_movie import Search, SimilarData


@pytest.fixture
def mock_search_movie():
    return Search("Ant man and the wasp", "movie")


@pytest.fixture
def movie_search():
    return Search("Ant man and the wasp", "movie")


def test_create_query(mock_search_movie):
    assert mock_search_movie.create_query() == "ant-man-and-the-wasp"


def mocked_requests_get(*args):
    if args[0] == f"https://api.themoviedb.org/3/search/movie?api_key=fakeapikey&query=the-transporter":
        return Response().json(status_code=200)


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_return_movie_id(mock_get, movie_search):
    movie_search.query = "The Transporter"
    assert movie_search.return_id == "4108"


def test_similar_movie_data_class():
    data = SimilarData("Ant man", "Short overview", "20.06.2018", "/poster.png")
    assert data.title == "Ant man"
    assert data.overview == "Short overview"
    assert data.release_date == "20.06.2018"
    assert data.poster == "/poster.png"


