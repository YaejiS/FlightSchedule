from flask_login import current_user
from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp
)
from .models import User
import pyotp
import re
from string import ascii_lowercase, digits


class SearchForm(FlaskForm):

    originplace = StringField(
        "Origin", validators=[InputRequired(), Length(min=3, max=3), Regexp('^\w+', message="Username must contain only letters numbers or underscore")]
    )

    destinationplace = StringField(
        "Destination", validators=[InputRequired(), Length(min=3, max=3), Regexp('^\w+')]
    )
    # outboundpartialdate = DateTimeField('Deprt', widget=DateTimePickerWidget())
    # outboundpartialdate = DateField(DateField('Pick a Date', format="%m/%d/%Y"))


    outboundpartialdate = StringField(
        "Depart Date", validators=[InputRequired(), Length(min=1, max=100)]
    )

    returndate = StringField(
        "Return Date", validators=[InputRequired(), Length(min=1, max=100)]
    )

    submit = SubmitField("Search")

class ConfirmForm(FlaskForm):
    submit = SubmitField("Confirm")


class ReviewForm(FlaskForm):
    text = TextAreaField("Comment", validators=[InputRequired(), Length(min=5, max=500)])
    submit = SubmitField("Enter Comment")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()]
    )
    password = PasswordField(
        "Password", validators=[InputRequired()]
    )

    
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")
    
    def validate_password(self, password):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$,.^!%*#?&])[A-Za-z\d@$,.^!#%*?&]{8,32}$"

        if (len(password.data) < 8 and len(password.data) > 32) or re.search(re.compile(reg), password.data) is None:
            raise ValidationError("Password must include the following: between 8 and 32 characters long, at least 1 lowercase letter, at least 1 uppercase letter, at least 1 number, and at least 1 special character i.e. @$,.^!%*#?&")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    token = StringField('Token', validators=[
                        InputRequired(), Length(min=6, max=6)])
    submit = SubmitField("Login")

    def validate_token(self, token):
        user = User.objects(username=self.username.data).first()
        if user is not None:
            tok_verified = pyotp.TOTP(user.otp_secret).verify(token.data)
            if not tok_verified:
                raise ValidationError("Invalid Token")


class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")