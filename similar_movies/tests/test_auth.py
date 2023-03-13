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
    response = client.post('/login', data=dict(
        email='test@email.com',
        password='password'
    ), follow_redirects=True)

    assert response.status_code == 200


def test_login_invalid_email(client):
    """ Test login with not existing email address """
    response = client.post('/login', data=dict(
        email='test@email.com',
        password='password',
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b"Email does not exist" in response.data


def test_sign_up(client):
    """ Test sign up response status code """
    response = client.post('/signup', data=dict(
        email='test2@email.com',
        username='testuser',
        password1='password123',
        password2='password123',
    ))

    assert response.status_code == 200


def test_sign_up_too_short_password(client):
    """ Test sign up with too short password """
    response = client.post('/signup', data=dict(
        email='test3@email.com',
        username='testuser2',
        password1='abc',
        password2='abc',
    ))

    assert b"Password is too short" in response.data


def test_sign_up_not_the_same_password(client):
    """ Test sign up with not the same passwords """
    response = client.post('/signup', data=dict(
        email='test4@email.com',
        username='testuser3',
        password1='12345678',
        password2='123456789'
    ))

    assert b"Password are not the same!" in response.data

    
def test_logout(client):
    """ Test logout functionality """
    with client:
        response = client.get('/logout', follow_redirects=True)

        assert response.status_code == 200
