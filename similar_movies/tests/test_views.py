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


def test_blog_view(test_client):
    """ Test to check blog view status code """
    response = test_client.get('/blog')
    assert response.status_code == 200
    assert b"Blog" in response.data


def test_upComing_list_view(test_client):
    """ Test to check upComing_list view status code """
    response = test_client.get('/upcoming')
    assert response.status_code == 200
    assert b"Upcoming" in response.data


def test_save_show_view(test_client):
    """ Test to check save_show view status code
        It should return status code 302 becouse it
        redirect to 'auth.profile' """
    response = test_client.post('/save-show')
    assert response.status_code == 302


def test_delete_show_view(test_client):
    """ Test to check delete_show view status code
        It should return status code 302 becouse it
        redirect to 'auth.profile' """
    response = test_client.post('/delete-show/1')
    assert response.status_code == 302


def test_delete_post_view(test_client):
    """ Test to check delete_post view status code
        It should return status code 302 becouse it
        redirect to 'auth.profile' """
    response = test_client.post('/delete/post/1')
    assert response.status_code == 302


def test_delete_category_view(test_client):
    """ Test to check delete_category view status code
        It should return status code 302 becouse it
        redirect to 'auth.profile' """
    response = test_client.post('/delete/category/1')
    assert response.status_code == 302


def test_create_post_normal_user(test_client):
    """ Test to check if for normal user is not able to see
        view create_post app will move user on view "home" because normal user
        does not have access. Because of that it should return
        status code 302 and flash message """
    response = test_client.get('/create/post')
    assert response.status_code == 302


def test_create_category_normal_user(test_client):
    """ Test to check if for normal user is not able to see
        view create_category app will move user on view "home" because normal user
        does not have access. Because of that it should return
        status code 302 and flash message """
    response = test_client.get('/create/category')
    assert response.status_code == 302

