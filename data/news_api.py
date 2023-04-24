import flask
from flask import jsonify
from . import db_session
from .tasks import Tasks


blueprint = flask.Blueprint('news_api', __name__, template_folder='templates')


@blueprint.route('/check_task/<int:id>', methods=["GET", "POST"])
def check(id):
    db_sess = db_session.create_session()
    items = db_sess.query(Tasks).filter(id == Tasks.id)
    print(items)
    return jsonify(
        {
            'tasks': [item.to_dict()
                      for item in items]
        }
    )
