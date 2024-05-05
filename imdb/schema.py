import os
from datetime import datetime

from pymongo import MongoClient, ASCENDING

client = MongoClient(os.environ.get('ENV_DB_URL'))
db = client[os.environ.get('ENV_DB')]

# Define user collection schema
user_schema = {
    'username': {'type': 'string', 'required': True, 'unique': True},
    'password': {'type': 'string', 'required': True},
    'email': {'type': 'string', 'required': True, 'unique': True},
    'fullName': {'type': 'string'},
    'age': {'type': 'int'},
    'createdAt': {'type': 'date', 'default': datetime.utcnow},
    'updatedAt': {'type': 'date', 'default': datetime.utcnow}
}

# Create user collection
user_collection = db['users']

# Create indexes for unique fields
user_collection.create_index([('username', ASCENDING)], unique=True)
user_collection.create_index([('email', ASCENDING)], unique=True)

# Define movie collection schema
movie_schema = {
    'show_id': {'type': 'string'},
    'type': {'type': 'string'},
    'title': {'type': 'string'},
    'director': {'type': 'string'},
    'cast': {'type': 'list', 'schema': ['string']},
    'country': {'type': 'string'},
    'date_added': {'type': 'datetime'},
    'release_year': {'type': 'int'},
    'rating': {'type': 'string'},
    'duration': {'type': 'string'},
    'listed_in': {'type': 'list', 'schema': ['string']},
    'description': {'type': 'string'}
}

# Create movie collection
movie_collection = db['movies']

# Create indexes for unique fields
movie_collection.create_index([('show_id', ASCENDING)])
