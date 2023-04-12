from flask import Flask, render_template, request, make_response, session, redirect, jsonify, abort
import datetime as dt
from data import db_session
from data.users import User
from data.tasks import Tasks
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.login import LoginForm
from forms.task import TasksForm
from forms.news import NewsForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'timkarazvod'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(Tasks).filter(
            (Tasks.user == current_user) | (Tasks.is_private != True))
    else:
        news = db_sess.query(Tasks).filter(Tasks.is_private != True)
    return render_template('index.html', news=news)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('reg.html', title='Регистрация', form=form,
                                   message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('reg.html', title='Регистрация', form=form,
                                   message='Пользователь уже есть')
        user = User(
            login=form.login.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
    return render_template('reg.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        else:
            return render_template('log.html', message='Неправильный логин или пароль',
                                   form=form)
    return render_template('log.html', title='Авторизация', form=form)


@app.route('/tasks',  methods=['GET', 'POST'])
@login_required
def add_tasks():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = Tasks()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление задачи',
                           form=form)


@app.route('/tasks_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Tasks).filter(Tasks.id == id,
                                      Tasks.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def main():
    db_session.global_init('db/users1.db')
    app.run()


if __name__ == '__main__':
    main()
