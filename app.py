from flask import Flask, redirect, Blueprint, render_template, flash, url_for, request
from flask_bootstrap import Bootstrap
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from flask import Response
import os
from swerve import swerve


app = Flask(__name__)
Bootstrap(app)

app.secret_key = os.getenv('FLASK_SECRET', 'development')

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/swerve")
def swerve_to():
    return swerve(request.args.get('url_key'))


if __name__ == '__main__':
    app.run()
