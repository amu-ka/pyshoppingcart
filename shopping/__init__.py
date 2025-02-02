import os

from flask import Flask
from shopping import db, auth, product, cart


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    print(os.path.join(app.instance_path, 'shopping.sqlite'))# test
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'shopping.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    db.init_app(app)

    app.register_blueprint(auth.bp)

    app.register_blueprint(product.bp)
    app.add_url_rule('/', endpoint='index')

    app.register_blueprint(cart.bp)

    return app
