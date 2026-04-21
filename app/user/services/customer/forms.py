from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ....db_models import UserAccount

class SingUpForm(FlaskForm):
    username = StringField("Username",validators=[
                                        DataRequired(),
                                        Length(min=2, max=20)])
    
    email = StringField("Email",validators=[
                                        DataRequired(),
                                        Email()])
    
    password = PasswordField("Password",validators=[DataRequired(),
                                                   Length(min=8)])
    confirm_password = PasswordField("ConfirmPassword",validators=[DataRequired(),
                                                    EqualTo("password")])
    
    submit = SubmitField("Sing Up")

    def validate_email(self, email):
        existing_user_email = UserAccount.query.filter_by(
            email=email.data).first()
        if existing_user_email:
            raise ValidationError(f"Ezt az email címet már regisztrálták! <a href='{url_for('user.login')}'>Bejelentkezés</a>")


class LoginForm(FlaskForm):
    email = StringField("Email",validators=[
                                        DataRequired(),
                                        Email()])
    
    password = PasswordField("Password",validators=[DataRequired(),
                                                   Length(min=8)])
    
    remember = BooleanField("Remember Me")
    
    submit = SubmitField("Login")

