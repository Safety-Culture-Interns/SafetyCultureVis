from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.backend.APISync import API
from flaskr import db

bp = Blueprint('dash', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        return "hello matt"
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
