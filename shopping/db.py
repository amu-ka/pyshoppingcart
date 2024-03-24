import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'shopping_db' not in g:
        g.shopping_db= sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.shopping_db.row_factory = sqlite3.Row

    return g.shopping_db


def close_db(e=None):
    shopping_db = g.pop('shopping_db', None)

    if shopping_db is not None:
        shopping_db.close()


def init_db():
    shopping_db = get_db()

    with current_app.open_resource('schema.sql') as f:
        print(f.read().decode('utf8')) #test
        shopping_db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

