from flask_login import UserMixin

from . import db


class User(db.Model, UserMixin):
    """This model allows to create user with
    id as a primary key, email, username, password, profile image, bio"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(150))
    bio = db.Column(db.Text)
    country = db.Column(db.String(30))
    saved_movies = db.relationship(
        "SavedMovies", backref="user", cascade="all, delete-orphan"
    )
    watched_movies = db.relationship(
        "WatchedMovies", backref="user", cascade="all, delete-orphan"
    )


class SavedMovies(db.Model):
    """This model allows to save movies in user's profile"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    title = db.Column(db.String(200))
    image_url = db.Column(db.String(200))


class WatchedMovies(db.Model):
    """This model allows to add watched movies in user's profile"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    title = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
