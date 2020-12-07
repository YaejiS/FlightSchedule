from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from . import config
from .utils import current_time
import base64
import pyotp
import onetimepass


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    # 2-factor Authentication part
    otp_secret = db.StringField(required=True, min_length=16, max_length=16,
                                default=pyotp.random_base32())

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

    # returns an authentication URI.
    # This URI will be rendered as a QR code that you have to scan with your phone.
    def get_totp_uri(self):
        return 'otpauth://totp/flight:{0}?secret={1}&issuer=2FA-Demo' \
            .format(self.username, self.otp_secret)

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)


class Schedule(db.Document):
    traveller = db.ReferenceField(User, required=True)
    originplace = db.StringField(required=True, min_length=3, max_length=3)
    destinationplace = db.StringField(
        required=True, min_length=3, max_length=3)
    departure_date = db.StringField(required=True)
    price = db.StringField(required=True)


class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    carrier = db.StringField(required=True, min_length=1, max_length=100)
