import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    Response)

from flaskr.backend.APISync import API
from flaskr import db

bp = Blueprint('dash', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def index():
    if session.get('user_id') is not None:
        print(session.get('user_id'))
        return redirect("/dashboard/")
    else:
        return redirect(url_for('auth.login'))


@bp.route('/loading', methods=['GET', 'POST'])
def loading():
    api = API(session['user_id'], db.Users().get_api(session['user_id']))
    if not api.is_good_api_token():
        return redirect(url_for('auth.token'))
    else:
        return render_template('parts/progress.html')


@bp.route('/api_sync')
def api_sync():
    api = API(session['user_id'], db.Users().get_api(session['user_id']))

    def event_stream():
        # yield "data:{}\n\n".format("done")
        for number in api.sync_with_api():
            for numb in number:
                yield "data:" + str(round(numb)) + "\n\n"

    return Response(event_stream(), mimetype='text/event-stream')


# def progress():
#     def generate():
#         x = 0
#
#         while x <= 100:
#             yield "data:" + str(round(x)) + "\n\n"
#             x = x + 0.2
#             time.sleep(0.5)
#
#     return Response(generate(), mimetype='text/event-stream')
