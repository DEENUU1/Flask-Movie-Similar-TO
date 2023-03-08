from flask_login import UserMixin
from sqlalchemy import func

from . import db


class User(db.Model, UserMixin):
    """ This model allows to create user with id as a primary key, email, username and password """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())


class SavedMovies(db.Model):
    """ This model allows to save movies in user's profile """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    title = db.Column(db.String(200))
    image_url = db.Column(db.String(200))


class Category(db.Model):
    """ This model is connected with Post model and allows to create a category for a blog post """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


class BlogPost(db.Model):
    """ This model allows to create blog posts """
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'))
    title = db.Column(db.String(200))
    content = db.Column(db.Text())

