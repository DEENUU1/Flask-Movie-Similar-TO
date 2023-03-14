from similar_movies import create_app
import pytest


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


def test_home_view(test_client):
    """ Test for the main view status code
        pass if status code is equal to 200 """

    response = test_client.get('/')
    assert response.status_code == 200


def test_list_similar_shows_view(test_client):
    """ Test for view with similar movie list
        pass if status code is equal to 200"""
    response = test_client.get('/similar', query_string={'title': 'The Matrix',
                                                         'type': 'movie'})
    assert response.status_code == 200


def test_upComing_list_view(test_client):
    """ Test to check upComing_list view status code """
    response = test_client.get('/upcoming')
    assert response.status_code == 200
    assert b"Upcoming" in response.data


def test_popular_movie_list_view(test_client):
    """ Test to check popular_movies view status code """
    response = test_client.get('/popular/movies')
    assert response.status_code == 200

