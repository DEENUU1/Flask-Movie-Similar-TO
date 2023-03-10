from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from similar_movies import db, create_app
from .models import User, SavedMovies, WatchedMovies
from similar_movies.mail import send_email


auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ This view allows user to login """
    if request.method == 'POST':
        email = request.form.get('emailUser')
        password = request.form.get('passwordUser')
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Password is incorrect.", category='error')
        else:
            flash("Email does not exist", category="error")

    return render_template("login.html", user=current_user)


@auth.route('/signup', methods=['POST', 'GET'])
def sign_up():
    """ This view allows user to create a new account """
    if request.method == "POST":
        # Downloading data from form
        email = request.form.get("emailUser")
        username = request.form.get("usernameUser")
        password1 = request.form.get("passwordUser1")
        password2 = request.form.get("passwordUser2")
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        password_hash = generate_password_hash(password1, method='sha256')

        # Logic of sign up system
        if email_exists:
            flash("Email is already in database!", category='error')
        elif username_exists:
            flash("Username is already in database!", category='error')
        elif password1 != password2:
            flash("Password are not the same!", category='error')
        elif len(password1) < 8:
            flash("Password is too short. Password should have at least 8 characters.")
        else:
            new_user = User(email=email, username=username, password=password_hash)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            send_email("Similar Movies | Sign up", "Thank you for sign up on the website.", email)

            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """ This function allows user to logout """
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/profile')
@login_required
def profile():
    """ This view displays user's profile
        user can display and delete saved movies and tv shows """
    saved_shows = SavedMovies.query.filter_by(user_id=current_user.id).all()
    watched_shows = WatchedMovies.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html",
                           saved_shows=saved_shows,
                           watched_shows=watched_shows,
                           user=current_user)


@auth.route('/admin')
@login_required
def admin():
    """ This view display admin dashboard
        admin user is available to delete posts and categories """
    id = current_user.id
    if id == 1:
        available_users = User.query.filter_by().all()
        return render_template('admin.html',
                               user=current_user,
                               available_users=available_users)

    else:
        flash("You are not a admin user", category='error')
        return redirect(url_for('views.home'))


@auth.route('/delete-user/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    """ This function allows to remove movie or tv show from list for login user """
    user = User.query.get(id)
    if user.id != 1:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted", category='success')
        return redirect(url_for('auth.admin'))

    else:
        flash("You can't delete this account!", category='error')
        return redirect(url_for('auth.admin'))


@auth.route('/send-message/<int:id>', methods=['POST', 'GET'])
@login_required
def send_message(id):
    """ This function allows to send email for user in admin dashboard """
    if request.method == "POST":
        user = User.query.get(id)
        message = request.form.get("message")
        send_email("Static subject",
                   message,
                   user.email)
        flash("Message sent", category='success')
        return redirect(url_for('auth.admin'))

    else:
        return redirect(url_for('auth.admin'))

