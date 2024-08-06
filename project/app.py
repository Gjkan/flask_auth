import os

from flask import Flask, make_response, request

from db import create_data_base, create_user_table, create_blacklist_token_table, \
    get_conn_to_db, close_db


def create_app():
    app = Flask(__name__)
    app_settings = os.getenv(
        'APP_SETTINGS',
        'config.DevelopmentConfig'
    )
    app.config.from_object(app_settings)

    with app.app_context():
        create_data_base()
        create_user_table()
        create_blacklist_token_table()
        close_db()

    return app


app = create_app()
tokens = ['1', '2', '3']


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.values.get('email')
        password = request.values.get('password')
        sql = 'INSERT INTO user (id, email, password, admin) VALUES(?, ?, ?, ?)'
        with app.app_context():
            db_conn = get_conn_to_db()
            cursor = db_conn.cursor()
            cursor.execute(sql, (1, email, password, False))
            db_conn.commit()
            close_db()

        return make_response('добавлен в бд')
    elif request.method == 'GET':
        return make_response('hhhh')


def test_registration(client):
    response = client.post('/register', data={'email': 'mail', 'password': 123})
    assert 'добавлен в бд'.encode('utf-8') in response.data


client = app.test_client()
test_registration(client=client)
