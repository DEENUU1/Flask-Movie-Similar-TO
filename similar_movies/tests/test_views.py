from similar_movies import create_app
from similar_movies import db
from similar_movies.models import User
import pytest
from werkzeug.security import generate_password_hash
from similar_movies import create_app

def test_home_view():
    """ Test for the main view status code
        pass if status code is equal to 200 """
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200


def test_list_similar_movies_view():
    """ Test for view with similar movie list
        pass if status code is equal to 200"""
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        response = test_client.get('/similar', query_string={'movie_name': 'The Matrix'})
        assert response.status_code == 200

@pytest.fixture
def logged_in_client():
    # create a test user
    user = User(username='testuser', password=generate_password_hash('testpassword'))
    db.session.add(user)
    db.session.commit()

    # log in the user using the test client
    with app.test_client() as client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
        with client.session_transaction() as session:
            session['_user_id'] = user.id
        yield client

    # clean up the test user
    db.session.delete(user)
    db.session.commit()

