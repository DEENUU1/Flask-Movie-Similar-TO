from flask import Blueprint, render_template, request, redirect, url_for
from similar_movies.search_movie import SimilarMovies


views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def home():
    """ This is a main view which display form to search a movie """
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        return redirect(url_for('views.list_similar_movie', movie_name=movie_name))
    else:
        return render_template('home.html')


@views.route('/similar', methods=['GET'])
def list_similar_movie():
    """ This view allows to display list of similar movies """
    movie_name = request.args.get("movie_name")
    similar_movies = SimilarMovies(movie_name)
    return_similar_movies = similar_movies.return_similar_movies()

    return render_template('list_similar_movie.html',
                           return_similar_movies=return_similar_movies,
                           movie_name=movie_name)