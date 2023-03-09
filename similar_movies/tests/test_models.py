from similar_movies.models import User, SavedMovies, Post, Category


def test_user_model():
    """ Simple model test to test creating a new user """
    user_1 = User(email='test@email.com',
                  username='testuser',
                  password='test_password')

    assert user_1.username == 'testuser'
    assert user_1.password == 'test_password'
    assert user_1.email == 'test@email.com'


def test_saved_movies_model():
    """ Simple model test to test saving a movie """
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


def test_create_category():
    """ Simple model test to test creating a blog category """
    category_1 = Category(
        id=1,
        name='Document'
    )
    assert category_1.name == 'Document'
    assert category_1.id == 1


def test_create_post():
    """ Simple model test to test creating a blog post """
    post_1 = Post(
        id=1,
        category_id=1,
        title='Test post',
        content='test content text',
    )
    assert post_1.id == 1
    assert post_1.category_id == 1
    assert post_1.title == "Test post"
    assert post_1.content == "test content text"



