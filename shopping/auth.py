import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from shopping.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    customer_id = session.get('customer_id')

    if customer_id is None:
        g.customer = None
    else:
        g.customer = get_db().execute(
            'SELECT * FROM customer WHERE id = ?', (customer_id,)
        ).fetchone()


#Require Authentication in Other Views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.customer is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'email is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO customer (name, email, username, password) VALUES (?, ?, ?, ?)",
                    (name, email, username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                if db.IntegrityError.__getattribute__() == 'username':
                    error = f"Customer {username} is already registered."
                elif db.IntegrityError.__getattribute__() == 'email':
                    error = f"email {email} is already used. You may have been registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        customer = db.execute(
            'SELECT * FROM customer WHERE username = ?', (username,)
        ).fetchone()

        if customer is None:
            error = 'Incorrect username.'
        elif not check_password_hash(customer['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['customer_id'] = customer['id']
            return redirect(url_for('product.index'))

        flash(error)

    return render_template('auth/login.html')


#To log out, you need to remove the user id from the session. Then load_logged_in_user won’t load a user on subsequent requests.
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('product.index'))


