import pytest
from similar_movies import create_app


@pytest.fixture
def client():
    """ Test client """
    create_app().config['TESTING'] = True
    client = create_app().test_client()
    yield client


def test_login(client):
    """ Test login response status code """
    response = client.get('/login')
    assert response.status_code == 200


def test_sign_up(client):
    """ Test sign up response status code """
    response = client.get('/signup')
    assert response.status_code == 200


def test_logout(client):
    """ Test logout functionality """
    with client:
        response = client.get('/logout', follow_redirects=True)

        assert response.status_code == 200
