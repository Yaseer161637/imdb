import os
from bson.objectid import ObjectId
from flask import Flask
from flask_login import LoginManager

from imdb.models import User
from .movie.views import movie_blueprint
from .users.views import users_blueprint

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(movie_blueprint)

login_manager.login_view = "users.login"


@login_manager.user_loader
def load_user(user_id):
    user = User.get_user({'_id': ObjectId(user_id)})
    if user:
        return user
    return None
