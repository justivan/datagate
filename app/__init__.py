import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # blueprints
    from app.main import main
    app.register_blueprint(main)
    from app.auth import auth
    app.register_blueprint(auth)
    from app.api import api
    app.register_blueprint(api)


    return app

from app import models