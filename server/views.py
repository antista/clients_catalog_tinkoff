from functools import wraps

from flask import Response, redirect, render_template, request, url_for, flash, abort

from .models import User
from .wsgi import app

users_passwords = dict()
sessions = dict()


def check_auth(username, password):
    if username in users_passwords.keys():
        return users_passwords[username] == password
    users_passwords[username] = password
    return True


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth is None or not check_auth(auth.username, auth.password):
            return authenticate()
        if auth.username not in sessions.keys():
            sessions[auth.username] = User(auth.username)
        return f(*args, **kwargs)

    return decorated


def get_login():
    auth = request.authorization
    return auth.username if auth is not None else None


@app.route('/')
@requires_basic_auth
def index():
    return redirect(url_for('authed_index', login=get_login()))


@app.route('/<login>')
@requires_basic_auth
def authed_index(login):
    if get_login() != login:
        abort(404)
    return render_template('index.html', user=sessions[login])


@app.route('/<login>/create', methods=['POST'])  # pragma: no cover
def create(login):
    name = request.form['name']
    phone_number = request.form['phone_number']
    email = request.form['email']
    try:
        sessions[login].create_client(name, phone_number, email)
    except FileExistsError:
        flash('This email or phone number is already exist in your clients base')
    return redirect(url_for('authed_index', login=login))


@app.route('/<login>/delete/<client_id>')
def delete(login, client_id) -> Response:
    sessions[login].delete_client(client_id)
    return redirect(url_for('authed_index', login=login))
