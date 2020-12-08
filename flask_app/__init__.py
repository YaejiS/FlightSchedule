# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman
from flask_mail import Mail
from werkzeug.utils import secure_filename
# from flask_bootstrap import Bootstrap
# from flask_wtf import Form
# from wtforms.fields import DateField

# stdlib
from datetime import datetime
import os

# local
from .client import FlightClient

mail = Mail()
#talisman = Talisman()
db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
flight_client = FlightClient(
    "f511e4e457mshbb220780db8fe47p1fd209jsnd4a2de0f8ae8")

from .users.routes import users
from .flights.routes import flights


def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST")

    # app.run(debug=True, port=33507)
    app.config.from_pyfile("config.py", silent=False)
    # Bootstrap(app)

    if test_config is not None:
        app.config.update(test_config)

    csp = {
        'default-src': [
            '\'self\'',
            '\'unsafe-inline\'',
            'stackpath.bootstrapcdn.com',
            'code.jquery.com',
            'cdn.jsdelivr.net',
            'cdn-na.infragistics.com',
            'cdnjs.cloudflare.com',
            'unpkg.com', 
            'screenfeedcontent.blob.core.windows.net',
            'ajax.aspnetcdn.com',
            'use.fontawesome.com'],
        'img-src': '*',
    }

    #talisman.init_app(app, content_security_policy=csp)

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'cmsc388j@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Cmsc388j!!!!'
    app.config['MAIL_DEFAULT_SENDER'] = 'cmsc388j@gmail.com'
    app.config['MAIL_USE_SSL'] = True

    mail.init_app(app)    

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(flights)

    app.register_error_handler(404, page_not_found)

    login_manager.login_view = 'users.login'

    return app
