import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    from .views import views
    app.register_blueprint(views)

    return app
