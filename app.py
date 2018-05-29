from flask import Flask, Response, redirect, Blueprint, render_template, flash, url_for, request
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_bootstrap import Bootstrap
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from flask_sqlalchemy import SQLAlchemy
from oauth import oauth_bp, login_required
import os
from utils.dict import Default


app = Flask(__name__)
Bootstrap(app)
app.register_blueprint(oauth_bp)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import *


@app.route("/")
@login_required
def index():
    return render_template('index.html')


@app.route("/swerve")
@login_required
def swerve_to():
    swerve_string = request.args.get('swerve_string')
    params = swerve_string.split(' ')
    opts = {}
    for i, opt in enumerate(params[1:]):
        opts['opt' + str(i + 1)] = opt
    return swerve(params[0], **opts)


@app.route("/add")
@login_required
def add_shortcut():
    errors = []
    new_shortcut = request.args.get('new_shortcut').split(' ', 1)
    key = new_shortcut[0]
    url_template = new_shortcut[1]

    # if key already exists, we'll redirect to the UI to edit
    if len(db.session.query(Shortcut).filter(Shortcut.key==key).all()) > 0:
        # errors.append("Item already exists in database.")
        # return render_template('index.html', errors=errors)  # TODO: redirect to edit view once it exists
        return swerve(key)

    try:
        shortcut = Shortcut(key=key,url_template=url_template)
        db.session.add(shortcut)
        db.session.commit()
    except:
        errors.append("Unable to add item to database.")

    return render_template('index.html', errors=errors)


def swerve(key, **kwargs):
    shortcut = db.session.query(Shortcut).filter(Shortcut.key==key).all()

    if len(shortcut) == 0:
        return render_template('index.html')  # TODO: redirect to an add view once it exists

    redirect_url = shortcut[0].url_template.format_map(Default(kwargs))
    return redirect(redirect_url, code=302)


if __name__ == '__main__':
    app.run()
