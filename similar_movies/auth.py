from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from similar_movies import db
from .models import User, SavedMovies, WatchedMovies
from similar_movies.email import send_email
from .forms import RegisterForm, LoginForm, ProfileDetailsForm
from flask_bcrypt import Bcrypt


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """This view allows user to login"""
    form = LoginForm()
    bcrypt = Bcrypt()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You are logged in", category="success")
                return redirect(url_for("views.home"))

    return render_template("login.html", form=form, user=current_user)


@auth.route("/signup", methods=["POST", "GET"])
def sign_up():
    """This view allows user to create a new account"""
    form = RegisterForm()
    bcrypt = Bcrypt()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(
            email=form.email.data, username=form.username.data, password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        send_email(
            "Similar Movies | Sign Up",
            f"Thanks for sign up {new_user.username}",
            new_user.email,
        )
        flash("Welcome on the website", category="success")
        return redirect(url_for("views.home"))
    return render_template("signup.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    """This function allows user to logout"""
    logout_user()
    flash("You have been logged out", category="success")
    return redirect(url_for("views.home"))


@auth.route("/profile")
@login_required
def profile():
    """This view displays user's profile
    user can display and delete saved movies and tv shows"""
    saved_shows = SavedMovies.query.filter_by(user_id=current_user.id).all()
    watched_shows = WatchedMovies.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "profile.html",
        saved_shows=saved_shows,
        watched_shows=watched_shows,
        user=current_user,
    )


@auth.route("/profile/details", methods=["POST", "GET"])
@login_required
def profile_details():
    """This view allows login user to edit additional information"""
    form = ProfileDetailsForm()
    if form.validate_on_submit():
        user_data = User.query.get(current_user.id)

        # This if statements allows to update only 1 element without deleting others
        if form.bio.data:
            user_data.bio = form.bio.data
        if form.country.data:
            user_data.country = form.country.data

        db.session.commit()
        flash("Information saved", category="success")
        return redirect(url_for("auth.profile"))

    return render_template("profile_details.html", form=form, user=current_user)


@auth.route("/admin")
@login_required
def admin():
    """This view display admin dashboard
    admin user is available to delete posts and categories"""
    user_id = current_user.id
    if user_id == 1:
        available_users = User.query.filter_by().all()
        return render_template("admin.html", available_users=available_users)
    else:
        flash("You are not a admin user", category="error")
        return redirect(url_for("views.home"))


@auth.route("/admin/users/<int:user_id>")
@login_required
def user_details(user_id: int):
    """This view allows admin user to check information about every single user"""
    admin_id = current_user.id
    if admin_id == 1:
        user_info = User.query.get(user_id)
        user_saved_shows = SavedMovies.query.filter_by(user_id=user_info.id).all()
        user_watched_shows = WatchedMovies.query.filter_by(user_id=user_info.id).all()
        return render_template(
            "user_details.html",
            user_info=user_info,
            user_saved_shows=user_saved_shows,
            user_watched_shows=user_watched_shows,
        )
    else:
        flash("You are not a admin user", category="error")
        return redirect(url_for("views.home"))


@auth.route("/delete-user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id: int):
    """This function allows to remove movie or tv show from list for login user"""
    user = User.query.get(user_id)
    if user.id != 1:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted", category="success")
        return redirect(url_for("auth.admin"))

    else:
        flash("You can't delete this account!", category="error")
        return redirect(url_for("auth.admin"))


@auth.route("/send-message/<int:user_id>", methods=["POST", "GET"])
@login_required
def send_message(user_id: int):
    """This function allows to send email for user in admin dashboard"""
    if request.method == "POST":
        user = User.query.get(user_id)
        message = request.form.get("message")
        send_email("Static subject", message, user.email)
        flash("Message sent", category="success")
        return redirect(url_for("auth.admin"))

    else:
        return redirect(url_for("auth.admin"))
