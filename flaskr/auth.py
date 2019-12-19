import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr import db, APISync

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        return redirect(url_for('callbacks.dashboard'))
    else:
        return redirect(url_for('auth.login'))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        api = request.form['api']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.Users().user_exists(username):
            error = 'User {} is already registered.'.format(username)
        elif not APISync.API().is_good_api_token(api):
            error = 'Token {} was not accepted.'.format(api)
        elif not is_good_credential(username):
            error = 'Username must be 8 characters long, and include a number'
        elif not is_good_credential(password):
            error = 'Password must be 8 characters long, and include a number'
        if error is None:
            db.Users().add_user(username, password, api)
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/token', methods=('GET', 'POST'))
def token():
    if request.method == 'POST':
        api = request.form['api']
        error = None
        if APISync.API().is_good_api_token(api):
            db.Users().update_api(session['user_id'], api)
            return redirect(url_for('dash.loading'))
        else:
            error = 'Wrong or expired API'
        flash(error)
    return render_template('auth/token.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.Users().get_user(username, password)

        if user is None:
            error = 'Incorrect credentials.'
        if error is None:
            session.clear()
            session['user_id'] = user['username']
            return redirect(url_for('dash.loading'))
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.Users().get_user_by_id(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dash.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


def is_good_credential(credential):
    if len(credential) < 8:
        return False
    else:
        return any(char.isdigit() for char in credential)
