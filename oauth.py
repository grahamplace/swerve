import os
from datetime import timedelta
from functools import wraps
from flask import Blueprint, jsonify, redirect, request, session, url_for
from flask_oauthlib.client import OAuth

oauth_bp = Blueprint('oauth', __name__)

oauth = OAuth(oauth_bp)
google = oauth.remote_app(
    'google',
    consumer_key=os.getenv('GOOGLE_OAUTH_ID', 'development'),
    consumer_secret=os.getenv('GOOGLE_OAUTH_SECRET', 'development'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v2/',
    authorize_url='https://accounts.google.com/o/oauth2/auth?prompt=consent',
    access_token_url='https://accounts.google.com/o/oauth2/token',
)

APPROVED_EMAILS = ['grahamgplace@gmail.com', 'graham@opendoor.com']


@oauth_bp.before_request
def session_lifetime():
    session.permanent = True
    session.modified = True
    oauth_bp.permanent_session_lifetime = timedelta(days=2)


@oauth_bp.route('/auth/user')
def auth_user():
    return jsonify(session.get('oauth.user'))


@oauth_bp.route('/auth/google')
def auth_google():
    session['oauth.return_to'] = request.referrer or '/'
    return google.authorize(callback=url_for('.auth_google_callback', _external=True))


@oauth_bp.route('/auth/google/callback')
def auth_google_callback():
    res = google.authorized_response()
    session['oauth.access_token'] = res['access_token']
    user = google.get('userinfo')
    if user.data['email'] in APPROVED_EMAILS:
        session['oauth.user'] = user.data

    return redirect(session.get('oauth.return_to'))


@google.tokengetter
def session_google_token():
    return (session.get('oauth.access_token'), '')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'oauth.user' not in session:
            if request.accept_mimetypes.best == 'text/html':
                return redirect(url_for('oauth.auth_google'))
            return 'Unauthorized', 401
        return f(*args, **kwargs)
    return decorated_function
