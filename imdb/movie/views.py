import csv
import os

from flask import render_template, request, \
    Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from pymongo import MongoClient, ASCENDING, DESCENDING

from ..models import FileProgress

client = MongoClient(os.environ.get('ENV_DB_URL'))
db = client[os.environ.get('ENV_DB')]
movie_collection = db.movie
file_collection = db.file

movie_blueprint = Blueprint(
    'movie', __name__,
    template_folder='templates'
)

LIMIT = 10


def get_movies():
    """
        Retrieve movies from the database based on pagination and sorting parameters.

        Returns:
            tuple: A tuple containing a list of movies and a boolean indicating if there are more movies available.
    """

    page = int(request.args.get("page", 1))
    sort = request.args.get('sort')
    order = request.args.get('order')
    skip = page * LIMIT
    movies = movie_collection.find({}, {'_id': 0})
    if sort and order:
        sort_criteria = [(sort, ASCENDING)] if order == 'asc' else [(sort, DESCENDING)]
        movies.sort(sort_criteria)
    movies = list(movies.skip(skip).limit(LIMIT))
    has_next = movie_collection.count_documents({}) > (skip + LIMIT)
    return movies, has_next


@movie_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
        Render the dashboard page with paginated and sorted movie data.

        Returns:
            str: Rendered dashboard page template.
    """

    if request.method == 'POST':
        pass  # future implementation if require

    movies, has_next = get_movies()
    headers = list(movies[0].keys()) if movies else []
    curr_page = int(request.args.get("page", 1))
    has_prev = curr_page > 1
    sort = request.args.get('sort')
    order = request.args.get('order')
    data = {
        'has_prev': has_prev,
        'has_next': has_next,
        'curr_page': curr_page,
        'sort': sort,
        'order': order,
        'headers': headers,
        'movies': movies,

    }
    return render_template("dashboard.html", data=data)


@movie_blueprint.route('/csv_upload', methods=['POST'])
@login_required
def upload_csv():
    """
        Handle CSV file upload, parsing, and insertion into the database.

        Returns:
            str: Redirect to the dashboard or an error page.
    """

    CHUNK_SIZE = 1000
    if 'csv_file' not in request.files:
        flash('Upload valid csv file')
        return render_template('error.html', error="Invalid file")

    file = request.files.get('csv_file')
    if file:
        file_path = os.path.join(file.filename)
        file.save(file_path)
        f = FileProgress(username=current_user.username, filepath=file_path, added_count=0, status='Progress')
        f.save()
        with open(file_path, 'r') as csvfile:
            csv_data = csv.DictReader(csvfile)
            chunk = []
            for row in csv_data:
                chunk.append(row)
                if len(chunk) >= CHUNK_SIZE:
                    f.update(f.created_at, {'added_count': f.added_count + len(chunk)})
                    db.movie.insert_many(chunk)
                    chunk = []

            if chunk:
                f.update(f.created_at, {'added_count': f.added_count + len(chunk), 'status': 'Completed'})
                db.movie.insert_many(chunk)

        # os.remove(file_path)
        return redirect(url_for('movie.dashboard'))


@movie_blueprint.route('/file_progress', methods=['POST', 'GET'])
@login_required
def file_progress():
    """
        Retrieve and render file upload progress for the current user.

        Returns:
            str: Rendered file progress page template.
    """

    error = None
    fp = list(file_collection.find({'username': current_user.username}, {'_id': 0}))
    headers = list(fp[0].keys()) if fp else []
    data = {'headers': headers,
            'files': fp}
    return render_template('file_progress.html', error=error, data=data)
