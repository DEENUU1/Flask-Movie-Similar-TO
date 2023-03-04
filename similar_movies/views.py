from flask import Blueprint, render_template, request, redirect, url_for, flash
from similar_movies.search_movie import SimilarMovies
from flask_login import current_user, login_required
from similar_movies.models import SavedMovies
from similar_movies import db

views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def home():
    """ This is a main view which display form to search a movie """
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        return redirect(url_for('views.list_similar_movie', movie_name=movie_name))
    else:
        return render_template('home.html',
                               user=current_user)


@views.route('/similar', methods=['GET'])
def list_similar_movie():
    """ This view allows to display list of similar movies """
    movie_name = request.args.get("movie_name")
    similar_movies = SimilarMovies(movie_name)
    return_similar_movies = similar_movies.return_similar_movies()

    return render_template('list_similar_movie.html',
                           return_similar_movies=return_similar_movies,
                           movie_name=movie_name,
                           user=current_user)


@views.route('/save-movie', methods=['POST'])
@login_required
def save_movie():
    title = request.form.get('title')
    poster = request.form.get('poster')
    save_movie = SavedMovies(user_id=current_user.id, title=title, image_url=poster)
    db.session.add(save_movie)
    db.session.commit()
    flash("Movie saved in your profile", category='success')
    return redirect(url_for('auth.profile'))


@views.route('/delete-movie/<int:id>', methods=['POST'])
@login_required
def delete_movie(id):
    movie = SavedMovies.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    flash("Movie deleted from your profile", category='success')
    return redirect(url_for('auth.profile'))