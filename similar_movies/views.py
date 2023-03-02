from flask import Blueprint, render_template, request, redirect
from similar_movies.search_movie import SimilarMovies, SearchMovie


views = Blueprint('views', __name__)


# @views.route('/', methods=['POST', 'GET'])
# def home():
#     if request.method == 'POST':
#         movie_name = request.POST['movie_name']
#         return movie_name
#     else:
#         return render_template('home.html')
#     return redirect()


@views.route('/similar', methods=['GET'])
def list_similar_movie():
    similar_movies = SimilarMovies(home())
    return_similar_movies = similar_movies.return_similar_movies()

    return render_template('list_similar_movie.html',
                           return_similar_movies=return_similar_movies)