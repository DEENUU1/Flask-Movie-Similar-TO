from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from similar_movies import db
from similar_movies.models import SavedMovies
from similar_movies.search_movie import Similar, UpComingMovies

views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def home():
    """ This is a main view which display form to search a movie or tv shows"""
    if request.method == 'POST':
        title = request.form['title']
        type = request.form['type']
        return redirect(url_for('views.list_similar_show', title=title, type=type))
    else:
        return render_template('home.html',
                               user=current_user)


@views.route('/similar', methods=['GET'])
def list_similar_show():
    """ This view allows to display list of similar movies or tv shows """
    title = request.args.get("title")
    type = request.args.get("type")
    similar_shows = Similar(title, type)
    try:
        return_similar_shows = similar_shows.return_similar_shows()
    except IndexError:
        flash("0 similar shows", category='error')
    return render_template('list_similar.html',
                           return_similar_shows=return_similar_shows,
                           title=title,
                           user=current_user)


@views.route('/upcoming', methods=['GET'])
def upComing_list():
    """ This view is displaying upcoming movies. It has a pagination when 1 page is 1 page from API """
    page = request.args.get('page', 1, type=int)
    upcoming_movies = UpComingMovies().return_upcoming_movies(page=page)
    return render_template("upcoming_list.html",
                           movies=upcoming_movies,
                           user=current_user,
                           current_page=page)


@views.route('/save-show', methods=['POST'])
@login_required
def save_show():
    """ This function allows to add movie or tv show to list for login user """
    title = request.form.get('title')
    poster = request.form.get('poster')
    save_show = SavedMovies(user_id=current_user.id, title=title, image_url=poster)
    db.session.add(save_show)
    db.session.commit()
    flash("Show saved in your profile", category='success')
    return redirect(url_for('auth.profile'))


@views.route('/delete-show/<int:id>', methods=['POST'])
@login_required
def delete_show(id):
    """ This function allows to remove movie or tv show from list for login user """
    show = SavedMovies.query.get(id)
    db.session.delete(show)
    db.session.commit()
    flash("Show deleted from your profile", category='success')
    return redirect(url_for('auth.profile'))