from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr import register_api_sync

bp = Blueprint('dash', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        return "hello matt"
    else:
        return redirect(url_for('auth.login'))


@bp.route('/loading')
def loading():
    register_api_sync()
    return render_template('parts/progress.html')
