from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from .models import User
from flask_wtf.file import FileField, FileRequired


class RegisterForm(FlaskForm):
    """ This form allows to Sign Up """
    email = EmailField(validators=[
            InputRequired()], render_kw={'placeholder': "Email"})
    username = StringField(validators=[
            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
            InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        """ This method is checking if email already exist in database"""
        existing_user_email = User.query.filter_by(
            email=email.data).first()
        if existing_user_email:
            raise ValidationError(
                'That email already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    """ This form allows to log in """
    email = EmailField(validators=[
            InputRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[
            InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


class ProfileDetailsForm(FlaskForm):
    """ This form allows login user to change additional information on the profile """
    bio = TextAreaField(render_kw={"placeholder": "Bio"})
    country = StringField(render_kw={"placeholder": "Country"})
    submit = SubmitField('Submit')