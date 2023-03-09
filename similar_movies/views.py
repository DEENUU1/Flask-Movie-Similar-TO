from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy import or_

from similar_movies import db
from similar_movies.models import SavedMovies
from similar_movies.search_movie import Similar, UpComingMovies
from .models import Post, Category

views = Blueprint('views', __name__)

""" Main views """


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


@views.route('/blog', methods=['GET'])
def blog():
    """ This view allows to display posts on blog """
    posts = Post().query.filter_by().all()
    return render_template('blog.html',
                           posts=posts,
                           user=current_user)


""" Vies as a functions """


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


@views.route('/create/post', methods=['POST', 'GET'])
@login_required
def create_post():
    """ This view allows to create post. Only admin user are able to do it. """
    id = current_user.id
    if id == 1:
        category_list = Category.query.all()
        if request.method == "POST":
            title = request.form.get("title")
            category_id = request.form.get('category')
            content = request.form.get('content')

            post = Post(title=title, category_id=category_id, content=content)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('auth.admin'))
        return render_template('create_post.html',
                               user=current_user,
                               category_list=category_list)
    else:
        flash("You are not a admin user", category='error')
        return redirect(url_for('views.home'))


@views.route('/delete/post/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    """ This function allows to remove post """
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash("Post successfully removed", category='success')
    return redirect(url_for('auth.admin'))


@views.route('/create/category', methods=['POST', 'GET'])
@login_required
def create_category():
    """ This view allows to create category for a post. Only admin user are able to do it. """
    id = current_user.id
    if id == 1:
        if request.method == "POST":
            name = request.form.get('name')

            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('auth.admin'))
        return render_template('create_category.html',
                               user=current_user)
    else:
        flash("You are not a admin user", category='error')
        return redirect(url_for('views.home'))


@views.route('/delete/category/<int:id>', methods=['POST'])
@login_required
def delete_category(id):
    """ This function allows to remove category """
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()
    flash("Category successfully removed", category='success')
    return redirect(url_for('auth.admin'))


@views.route('/search', methods=['GET', 'POST'])
def search_post():
    """ This function allows to search posts
        query is searching for a pattern in post title and post content """
    if request.method == "POST":
        search_query = request.form['query']
        posts = Post.query.filter(or_(Post.title.ilike(f"%{search_query}%"), Post.content.ilike(f"%{search_query}%"))).all()
        return render_template('blog_search.html',
                               query=search_query,
                               posts=posts,
                               user=current_user)

