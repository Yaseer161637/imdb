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
    """
       Render the home page.
       Returns:
           str: Rendered home page template.
    """

    return render_template('home.html', error=None)


@users_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    """
        Handle user login.

        If user is already authenticated, redirect to dashboard.
        If form is submitted with valid credentials, log in the user.
        Otherwise, render the login page with appropriate error message.

        Returns:
            str: Rendered login page template or redirect to dashboard.
    """

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
    """
        Handle user logout.
        Log out the currently logged in user and redirect to login page.
        Returns:
            str: Redirect to login page.
    """

    logout_user()
    flash('You were logged out.')
    return redirect(url_for('users.login'))


@users_blueprint.route('/register', methods=['POST', 'GET'])
def register():
    """
        Handle user registration.
        If form is submitted with valid data, register the user and redirect to login page.
        Otherwise, render the registration page with the form.
        Returns:
            str: Rendered registration page template or redirect to login page.
    """

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        user.save()
        flash('Registered successfully.')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)
