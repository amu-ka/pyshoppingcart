from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from shopping.auth import login_required
from shopping.db import get_db

bp = Blueprint('product', __name__)


@bp.route('/')
def index():
    db = get_db()
    products = db.execute(
        'SELECT id, name, price, quantity, created, updated'
        ' FROM product'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('product/index.html', products=products)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        # created = datetime.now()
        # updated = created
        error = None

        if not name:
            error = 'Name is required.'
        if not price:
            error = 'Price is required.'
        if not quantity:
            error = 'Quantity is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO product (name, price, quantity)'
                ' VALUES (?, ?, ?)',
                (name, price, quantity)
            )
            db.commit()
            return redirect(url_for('product.index'))

    return render_template('product/create.html')


def get_product(id, check_customer=True):
    product = get_db().execute(
        'SELECT id, name, price, quantity, created'
        ' FROM product'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if product is None:
        abort(404, f"product id {id} doesn't exist.")

    if check_customer and g.customer['id'] != 1:
        abort(403)

    return product


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    product = get_product(id)

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        updated = datetime.now()
        error = None

        if not name:
            error = 'Name is required.'
        if not price:
            error = 'Price is required.'
        if not quantity:
            error = 'Quantity is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE product SET name = ?, price = ?, quantity = ?, updated = ?'
                ' WHERE id = ?',
                (name, price, quantity, updated, id)
            )
            db.commit()
            return redirect(url_for('product.index'))

    return render_template('product/update.html', product=product)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_product(id)
    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('product.index'))

