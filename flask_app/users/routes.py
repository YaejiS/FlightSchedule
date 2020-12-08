from flask import Blueprint, redirect, url_for, render_template, flash, request, session
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Mail, Message

from .. import bcrypt, mail
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm
from ..models import User

import pyotp
import qrcode
import qrcode.image.svg as svg
import qrcode.image.pil as pil
from io import BytesIO

users = Blueprint('users', __name__, static_folder='static',
                  template_folder='templates')


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("flights.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed)
        user.save()

        session['username'] = user.username
        return redirect(url_for('users.tfa'))

        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("flights.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("users.account"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("flights.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    username_form = UpdateUsernameForm()

    if username_form.validate_on_submit():
        # current_user.username = username_form.username.data
        current_user.modify(username=username_form.username.data)
        current_user.save()
        return redirect(url_for("users.account"))

    return render_template(
        "account.html",
        title="Account",
        username_form=username_form,
    )

@users.route('/twofactor')
def tfa():
    if 'username' not in session:
        return redirect(url_for('flights.index'))

    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0' # Expire immediately, so browser has to reverify everytime
    }

    return render_template('tfa.html'), headers


@users.route("/qr_code")
def qr_code():
    if 'username' not in session:
        return redirect(url_for('flights.index'))
    
    user = User.objects(username=session['username']).first()
    session.pop('username')

    uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(name=user.username, issuer_name='FlightSchedule')
    img = qrcode.make(uri, image_factory=svg.SvgPathImage)
    stream = BytesIO()
    img.save(stream)

    headers = {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0' # Expire immediately, so browser has to reverify everytime
    }

    code = qrcode.make(uri, image_factory=pil.PilImage)

    msg = Message("Hello from Flight Schedule", recipients=[user.email])
    
    msg.attach("img.png", 'image/png', code.tobytes())

    
    mail.send(msg)
        
    return stream.getvalue(), headers