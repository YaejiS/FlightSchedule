# from flask_bootstrap import Bootstrap
from flask_login import current_user
from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
# from wtforms.fields import DateField
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
# from datetime import datetimefield
# from flask.ext.admin.form import DateTimeField, DateTimePickerWidget
from .models import User
import pyotp


class SearchForm(FlaskForm):
    # country = StringField(
    #     "Country", validators=[InputRequired(), Length(min=2, max=2)]
    # )
    originplace = StringField(
        "Origin", validators=[InputRequired(), Length(min=3, max=3)]
    )
    destinationplace = StringField(
        "Destination", validators=[InputRequired(), Length(min=3, max=3)]
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
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
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
