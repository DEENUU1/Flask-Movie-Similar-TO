from similar_movies.models import User, SavedMovies


def test_user_model():
    user_1 = User(email='test@email.com',
                  username='testuser',
                  password='test_password')

    assert user_1.username == 'testuser'
    assert user_1.password == 'test_password'
    assert user_1.email == 'test@email.com'


def test_saved_movies_model():
    user_1 = User(id=1,
                  username='testuser',
                  email='test@email.com',
                  password='testpassword')

    movie_1 = SavedMovies(id=1,
                          user_id=user_1.id,
                          title="Test movie",
                          image_url='/asdasd002')

    assert movie_1.title == "Test movie"
    assert movie_1.image_url == '/asdasd002'
    assert movie_1.user_id == 1
