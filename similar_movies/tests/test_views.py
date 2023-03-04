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

