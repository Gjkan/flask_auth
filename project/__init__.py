import os

from flask import Flask, current_app
from project.db import create_data_base, create_user_table, create_blacklist_token_table, close_db_conn
from project.views import auth_blueprint
from flask_bcrypt import Bcrypt


def create_app():
    new_app = Flask(__name__)
    app_settings = os.getenv(
        'APP_SETTINGS',
        'project.config.DevelopmentConfig'
    )
    new_app.config.from_object(app_settings)
    with new_app.app_context():
        create_data_base()
        create_user_table()
        create_blacklist_token_table()
        close_db_conn()
        new_app.register_blueprint(auth_blueprint)
        bcrypt = Bcrypt(new_app)
        current_app.config['BCRYPT'] = bcrypt
    return new_app


if __name__ == 'main':
    app = create_app()
    app.run('localhost')
