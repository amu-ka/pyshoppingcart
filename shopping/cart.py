from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from shopping.auth import login_required
from shopping.db import get_db

bp = Blueprint('cart', __name__)

@bp.route('/cart')
@login_required
def cart():
    db = get_db()
    cart_items = db.execute(
        'SELECT o.id, p.name, p.price, o.quantity, o.total_price'
        ' FROM customer_order o'
        ' LEFT JOIN customer c on c.id = o.customer_id'
        ' LEFT JOIN product p ON p.id = o.product_id'
        ' WHERE o.order_com = \'N\''
    ).fetchall()
    return render_template('cart/cart.html', cart_items=cart_items)


@bp.route('/checkout')
@login_required
def checkout():
    return render_template('cart/checkout.html')

