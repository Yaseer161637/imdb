import os

from flask import flash, redirect, render_template, request, \
    url_for, Blueprint
from flask_login import login_required, login_user, logout_user, current_user
from pymongo import MongoClient

from imdb.models import User, bcrypt
from .forms import LoginForm, RegisterForm

client = MongoClient(os.environ.get('ENV_DB_URL'))
db = client[os.environ.get('ENV_DB')]

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)


@users_blueprint.route('/', methods=['GET'])
def home():
    return render_template('home.html', error=None)


@users_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('movie.dashboard'))

    error = None
    form = LoginForm(request.form)
    user = User.get_user({'username': form.username.data})
    if user and form.validate():
        user_pwd = user.password.encode('utf-8')
        if user and bcrypt.checkpw(request.form['password'].encode('utf-8'), user_pwd):
            login_user(user)
            flash('You were logged in.')
            return redirect(url_for('movie.dashboard'))
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('users.login'))


@users_blueprint.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        user.save()
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)
