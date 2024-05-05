import os
from datetime import datetime

import bcrypt
from bson import ObjectId
from flask_login import UserMixin
from pymongo import MongoClient

client = MongoClient(os.environ.get('ENV_DB_URL'))
db = client[os.environ.get('ENV_DB')]
user_collection = db.user
movie_collection = db.movie
file_collection = db.file


class User(UserMixin):
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.email = kwargs.get('email')
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        user_collection.insert_one(self.to_dict())

    @staticmethod
    def get_user(query):
        user = user_collection.find_one(query)
        return User(**user) if user else None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        if isinstance(self.id, ObjectId):
            return str(self.id)
        else:
            return None

    def to_dict(self):
        password = (bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
        return {
            'username': self.username,
            'password': password,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f"User(username='{self.username}', email='{self.email}')"


class Movie:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def save(self):
        db.movies.insert_one(**self.kwargs)

    def to_dict(self):
        return {
            'show_id': self.show_id,
            'type': self.type,
            'title': self.title,
            'director': self.director,
            'cast': self.cast,
            'country': self.country,
            'date_added': self.date_added,
            'release_year': self.release_year,
            'rating': self.rating,
            'duration': self.duration,
            'listed_in': self.listed_in,
            'description': self.description
        }

    def __repr__(self):
        return f"Movie(title='{self.title}', director='{self.director}')"


class FileProgress:
    def __init__(self, username, filepath, added_count, status):
        self.username = username
        self.filepath = filepath
        self.added_count = added_count
        self.status = status
        self.created_at = str(datetime.now())

    def save(self):
        file_collection.insert_one(self.to_dict())

    def update(self, query, fields):
        query = {'created_at': query}
        update = {'$set': fields}
        file_collection.update_one(query, update)

    def to_dict(self):
        return {
            'username': self.username,
            'filepath': self.filepath,
            'added_count': self.added_count,
            'status': self.status,
            'created_at': self.created_at
        }
