import flask
from flask import jsonify
from . import db_session
from .tasks import Tasks
from .users import User

# ----------------------------API-------------------------------------------------------------------
blueprint = flask.Blueprint('news_api', __name__, template_folder='templates')


@blueprint.route('/check_task/<int:id>', methods=["GET"])
def check(id):
    db_sess = db_session.create_session()
    items = db_sess.query(Tasks).filter(id == Tasks.user_id)
    return jsonify(
        {
            'tasks': [item.to_dict(only=('title', 'content', 'id'))
                      for item in items]
        }
    )


@blueprint.route('/check_link/<string:token>', methods=["GET"])
def check_link(token):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.bot_id == token).first()
    if user.linked:
        return jsonify(
            {'succes': False}
        )
    return jsonify(
        {'succes': True}
    )


@blueprint.route('/link/<string:token>', methods=["POST", "GET"])
def link(token):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.bot_id == token).first()
    if user:
        user.linked = True
        db_sess.commit()
        return jsonify(
            {'succes': True}
        )
    return jsonify(
        {'succes': False}
    )


@blueprint.route('/test/<int:id>', methods=["GET"])
def test(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id)
    return jsonify(
        {'user': user.to_dict()}
    )
