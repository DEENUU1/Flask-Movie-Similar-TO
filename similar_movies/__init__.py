import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)
    csrf = CSRFProtect()
    csrf.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    from .views import views

    app.register_blueprint(views)
    from .auth import auth

    app.register_blueprint(auth)
    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.context_processor
    def inject_user():
        return dict(user=current_user)

    return app


def create_database(app):
    """This function is check if a database exists.
    If it's not it create a new one."""
    if not os.path.exists("similar_movies" + DB_NAME):
        with app.app_context():
            db.create_all()
