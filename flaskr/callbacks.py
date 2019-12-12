import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    Response)

from flaskr.backend.APISync import API
from flaskr import db

bp = Blueprint('dash', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        return redirect("/dashboard/")
    else:
        return redirect(url_for('auth.login'))


@bp.route('/loading', methods=['GET'])
def loading():
    if request.method == 'GET':
        api = API(session['user_id'], db.Users().get_api(session['user_id']))
        if not api.is_good_api_token():
            return render_template('auth/token.html')
        else:
            return render_template('parts/progress.html')
@bp.route('/api_sync')
def api_sync():
    def event_stream():
        yield "data:{}\n\n".format("done")

    api = API(session['user_id'], db.Users().get_api(session['user_id']))
    api.sync_with_api()
    return Response(event_stream(), mimetype='text/event-stream')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.Users().get_user_by_id(user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view

