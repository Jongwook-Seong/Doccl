import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from venv.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id stored in the session, load the user object from
    the database into ``g.user``."""
    id = session.get('id')

    if id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (id,)
        ).fetchone()


@bp.route('/join', methods=('GET', 'POST'))
def join():
    """Register a new user.

    Validates that the user account is not already taken. Hashes the
    password for security.
    """
    if request.method == 'POST':
        id = request.form['id']
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        db.get_db()
        error = None

        if not id:
            error = 'Id is required.'
        elif not email:
            error = 'E-mail is required.'
        elif not password:
            error = 'Password is required.'
        elif not username:
            error = 'User name is required.'
        elif db.execute(
            'SELECT id FROM user WHERE id = ?', (id,)
        ).fetchone() is not None:
            error = 'User {0} is already joined.'.format(id)

        if error is None:
            # the account is available, store it in the database and go to
            # the login page
            db.execute(
                'INSERT INTO user (id, email, password, username) VALUES (?, ?, ?, ?)',
                (id, email, password, username)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/join.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user account to the session."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get.db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect e-mail.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template(url_for('index'))


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('index'))
