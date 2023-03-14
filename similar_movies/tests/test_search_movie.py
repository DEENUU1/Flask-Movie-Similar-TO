import pytest
from requests import Response
from unittest import mock
from unittest.mock import patch
from similar_movies.search_movie import Search, ShowData, BaseAPI, UpComingMovies, PopularMovies
import os


@pytest.fixture()
def mock_response():
    """ Fixture which initialise a response for mock testing """
    response = Response()
    response.status_code = 200
    response._content = b'{"results": [{"title": "Movie 1", "overview": "Overview 1", "poster_path": "poster1.jpg", "release_date": "2022-01-01"}]}'
    return response


@pytest.fixture()
def endpoint():
    """ Fixture with endpoint for UpComingMovies class """
    return BaseAPI(endpoint='https://api.themoviedb.org/3/movie/now_playing')


@patch('similar_movies.search_movie.get')
def test_base_api_get_data(mock_get, endpoint, mock_response):
    mock_get.return_value = mock_response
    data = endpoint._get_data()

    assert isinstance(data, list)
    assert data[0]['title'] == 'Movie 1'


def test_base_api_return_data(endpoint):
    with patch.object(endpoint, '_get_data',
                      return_value=[{'title': 'Movie 1', 'overview': 'Overview 1', 'poster_path': 'poster1.jpg', 'release_date': '2022-01-01'}]):
        data = endpoint.return_data()

    assert data[0].title == 'Movie 1'
    assert data[0].overview == 'Overview 1'
    assert data[0].poster == 'poster1.jpg'
    assert data[0].release_date == '2022-01-01'


def test_upcoming_movies_endpoint():
    upcoming_movies = UpComingMovies()
    assert upcoming_movies.endpoint == 'https://api.themoviedb.org/3/movie/now_playing'


def test_popular_movies_endpoint():
    popular_movies = PopularMovies()
    assert popular_movies.endpoint == 'https://api.themoviedb.org/3/movie/popular'


@pytest.fixture
def movie_search():
    """ Fixture for Search class """
    return Search("Ant man and the wasp", "movie")


def test_create_query(movie_search):
    """ Test for return query function """
    assert movie_search.create_query() == "ant-man-and-the-wasp"


def mocked_requests_get(*args):
    if args[0] == f"https://api.themoviedb.org/3/search/movie?api_key=fakeapikey&query=the-transporter":
        return Response().json(status_code=200)


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_return_movie_id(mock_get, movie_search):
    """ Test for return movie id function in Search class """
    movie_search.query = "The Transporter"
    assert movie_search.return_id == "4108"


def test_similar_movie_data_class():
    """ Test for ShowData dataclass """
    data = ShowData(title="Ant man",
                    overview="Short overview",
                    release_date="20.06.2018",
                    poster="/poster.png")
    assert data.title == "Ant man"
    assert data.overview == "Short overview"
    assert data.release_date == "20.06.2018"
    assert data.poster == "/poster.png"




