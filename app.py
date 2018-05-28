from flask import Flask, redirect, Blueprint, render_template, flash, url_for, request
from flask import Response
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_bootstrap import Bootstrap
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from flask.ext.sqlalchemy import SQLAlchemy
from oauth import oauth_bp, login_required
from swerve import swerve
import os


app = Flask(__name__)
Bootstrap(app)
app.register_blueprint(oauth_bp)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Shortcut


@app.route("/")
@login_required
def index():
    return render_template('index.html')


@app.route("/swerve")
@login_required
def swerve_to():
    return swerve(request.args.get('url_key'))


if __name__ == '__main__':
    app.run()
