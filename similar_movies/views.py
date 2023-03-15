from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from similar_movies import db
from similar_movies.models import SavedMovies, WatchedMovies
from similar_movies.search_movie import Similar, UpComingMovies, PopularMovies


views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def home():
    """ This is a main view which display form to search a movie or tv shows"""
    if request.method == 'POST':
        title = request.form['title']
        show_type = request.form['type']
        return redirect(url_for('views.list_similar_show', title=title, type=show_type))
    else:
        return render_template('home.html',
                               user=current_user)


@views.route('/similar', methods=['GET'])
def list_similar_show():
    """ This view allows to display list of similar movies or tv shows """
    try:
        title = request.args.get("title")
        show_type = request.args.get("type")
        similar_shows = Similar(title, show_type)
        try:
            return_similar_shows = similar_shows.return_similar_shows()
        except IndexError:
            flash("No similar shows for this title", category='error')
        return render_template('list_similar.html',
                               return_similar_shows=return_similar_shows,
                               title=title,
                               user=current_user)
    except UnboundLocalError:
        flash("Wrong title, try again", category='error')
        return redirect(url_for('views.home'))


@views.route('/upcoming', methods=['GET'])
def upComing_list():
    """ This view is displaying upcoming movies. It has a pagination where 1 page is 1 page from API """
    page = request.args.get('page', 1, type=int)
    upcoming_movies = UpComingMovies().return_data(page=page)
    return render_template("upcoming_list.html",
                           movies=upcoming_movies,
                           user=current_user,
                           current_page=page)


@views.route('/popular/movies', methods=['GET'])
def popular_movies():
    """ This view is displaying popular movies.
        It has a pagination where 1 page is 1 page from API """
    page = request.args.get('page', 1, type=int)
    popular_movie_list = PopularMovies().return_data(page=page)
    return render_template("popular_movies_list.html",
                           popular_movie_list=popular_movie_list,
                           user=current_user,
                           current_page=page)


@views.route('/save-show', methods=['POST'])
@login_required
def save_show():
    """ This function allows to add movie or tv show to list for login user """
    title = request.form.get('title')
    poster = request.form.get('poster')
    save_shows = SavedMovies(user_id=current_user.id, title=title, image_url=poster)
    db.session.add(save_shows)
    db.session.commit()
    flash("Show saved in your profile", category='success')
    return redirect(url_for('auth.profile'))


@views.route('/delete-show/<int:show_id>', methods=['POST'])
@login_required
def delete_show(show_id):
    """ This function allows to remove movie or tv show from list for login user """
    show = SavedMovies.query.get(show_id)
    if show.user_id != current_user.id:
        flash("You are not allowed to delete this show", category='error')
        return redirect(url_for('auth.profile'))
    db.session.delete(show)
    db.session.commit()
    flash("Show deleted from your profile", category='success')
    return redirect(url_for('auth.profile'))


@views.route('/save-watched', methods=['POST'])
@login_required
def save_watched_show():
    """ This function allows to add watched movie or tv show to list for login user """
    title = request.form.get('title')
    poster = request.form.get('poster')
    save_watched = WatchedMovies(user_id=current_user.id, title=title, image_url=poster)
    db.session.add(save_watched)
    db.session.commit()
    flash("Show saved in your watch history", category='success')
    return redirect(url_for('auth.profile'))


@views.route('/delete-watched/<int:show_id>', methods=['POST'])
@login_required
def delete_watched_show(show_id):
    """ This function allows to remove movie or tv show from watched list for login user """
    show = WatchedMovies.query.get(show_id)
    if show.user_id != current_user.id:
        flash("You are not allowed to delete this show", category='error')
        return redirect(url_for('auth.profile'))
    db.session.delete(show)
    db.session.commit()
    flash("Show deleted from your watch history", category='success')
    return redirect(url_for('auth.profile'))
