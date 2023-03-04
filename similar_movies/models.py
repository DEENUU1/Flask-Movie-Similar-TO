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
