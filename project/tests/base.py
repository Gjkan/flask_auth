from flask_testing import TestCase

from project import create_app
from project.db import delete_test_tables, create_data_base, create_user_table, create_blacklist_token_table, \
    close_db_conn


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app = create_app()
        with app.app_context():
            app.config.from_object('project.config.TestingConfig')
        return app

    def setUp(self):
        create_data_base()
        create_user_table()
        create_blacklist_token_table()
        close_db_conn()

    def tearDown(self):
        delete_test_tables()
