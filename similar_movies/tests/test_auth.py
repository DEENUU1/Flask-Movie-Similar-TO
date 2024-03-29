import pytest
from similar_movies import create_app


@pytest.fixture
def client():
    """Test client"""
    create_app().config["TESTING"] = True
    client = create_app().test_client()
    yield client


def test_login(client) -> None:
    """Test login response status code"""
    response = client.get("/login")
    assert response.status_code == 200


def test_sign_up(client) -> None:
    """Test sign up response status code"""
    response = client.get("/signup")
    assert response.status_code == 200


def test_logout(client) -> None:
    """Test logout functionality"""
    with client:
        response = client.get("/logout", follow_redirects=True)

        assert response.status_code == 200


def test_profile(client) -> None:
    """Test for profile view to check if a status code is equal to 200"""
    with client:
        response = client.get("/profile", follow_redirects=True)
        assert response.status_code == 200


def test_admin(client) -> None:
    """Test for admin view to check if a status code is equal to 200"""
    with client:
        response = client.get("/admin", follow_redirects=True)
        assert response.status_code == 200


def test_user_details(client) -> None:
    """Test for user_details view to check if a status code is equal to 200"""
    with client:
        response = client.get("/admin/users/1", follow_redirects=True)
        assert response.status_code == 200


def test_user_profile_details(client) -> None:
    """Test for profile_details view to check if a status code is equal to 200"""
    with client:
        response = client.get("/profile/details", follow_redirects=True)
        assert response.status_code == 200
