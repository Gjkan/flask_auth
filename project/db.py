from flask import current_app, g
from psycopg2 import sql, connect, ProgrammingError
from psycopg2.errors import DuplicateTable


def get_conn_to_db():
    if 'db_conn' not in g:
        g.db_conn = connect(database=current_app.config['DB_NAME'],
                            user=current_app.config['DB_USER'],
                            password=current_app.config['DB_PASSWORD'],
                            host=current_app.config['DB_HOST'],
                            port=current_app.config['DB_PORT'])
    return g.db_conn


def create_data_base():
    """Функции для создания базы данных."""
    conn = get_conn_to_db()
    if conn:
        cursor = conn.cursor()
        conn.autocommit = True
        db_name = current_app.config['DB_NAME']
        try:
            db_name = sql.Identifier(db_name)
            cursor.execute(sql.SQL('CREATE DATABASE {db_name}').format(db_name=db_name))
        except ProgrammingError:
            print(f"База данных {db_name} уже существует.")
        else:
            print(f"База данных {db_name} успешно создана.")
        cursor.close()
        close_db_conn()


def create_user_table():
    """Функции для создания таблицы user."""
    conn = get_conn_to_db()
    if conn:
        cursor = conn.cursor()
        user_table_name = sql.Identifier('user')
        try:
            cursor.execute(sql.SQL("""
                                  CREATE TABLE {user_table_name}
                                  (id SERIAL PRIMARY KEY,
                                   email varchar(100) NOT NULL,
                                   password varchar(100) NOT NULL,
                                   is_admin boolean NOT NULL DEFAULT FALSE,
                                   registration_date timestamptz NOT NULL;""").format(
                user_table_name=user_table_name, ))
        except DuplicateTable:
            print(f"Таблица {user_table_name} уже существует.")
        else:
            conn.commit()
            print(f"Таблица {user_table_name} успешно создана.")
        cursor.close()
        close_db_conn()


def create_blacklist_token_table():
    """Функции для создания таблицы blacklist_token."""
    conn = get_conn_to_db()
    if conn:
        cursor = conn.cursor()
        blacklist_token_table_name = sql.Identifier('blacklist_token_table')
        try:
            cursor.execute(sql.SQL("""
                                  CREATE TABLE {blacklist_token_table_name}
                                  (id SERIAL PRIMARY KEY,
                                   token varchar(500) NOT NULL,
                                   is_blacklisted boolean NOT NULL DEFAULT FALSE;""").format(
                blacklist_token_table_name=blacklist_token_table_name, ))
        except DuplicateTable:
            print(f"Таблица {blacklist_token_table_name} уже существует.")
        else:
            conn.commit()
            print(f"Таблица {blacklist_token_table_name} успешно создана.")
        cursor.close()
        close_db_conn()


def close_db_conn():
    db_conn = g.pop('db_conn', None)

    if db_conn is not None:
        db_conn.close()
