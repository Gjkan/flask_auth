from project.db import get_conn_to_db, close_db_conn
from psycopg2 import sql
from datetime import datetime, timedelta
import jwt
from flask import current_app


class User:
    """Класс для хранения методов, связанных с таблицей User"""

    @staticmethod
    def save(email, password):
        """Метод принимает email и password пользователя.
        Сохраняет пользователя в БД"""
        user_table_name = sql.Identifier(current_app.config['USER_TABLE_NAME'])
        conn = get_conn_to_db()
        cursor = conn.cursor()
        registration_date = datetime.utcnow()
        bcrypt = current_app.config.get('BCRYPT')
        password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode('utf-8')
        data = [email, password, registration_date]
        cursor.execute(sql.SQL("""INSERT INTO {user_table_name} 
                                  (email, password, registration_date)
                                  VALUES(%s, %s, %s);""").format(
            user_table_name=user_table_name), data)
        conn.commit()
        cursor.close()
        close_db_conn()

    @staticmethod
    def get_user_id_or_none(email):
        """Метод принимает email пользователя.
        Возвращает user_id пользователя или None, если такого пользователя нет в БД"""
        user_table_name = sql.Identifier(current_app.config['USER_TABLE_NAME'])
        conn = get_conn_to_db()
        cursor = conn.cursor()
        data = [email]
        cursor.execute(sql.SQL("""SELECT id FROM {user_table_name} WHERE
                                  email=%s;""").format(
            user_table_name=user_table_name), data)
        user_id = cursor.fetchone()
        cursor.close()
        close_db_conn()
        return user_id

    @staticmethod
    def get_user_dict_by_email(email):
        """Метод принимает email пользователя.
        Возвращает данные пользователя или None, если такого пользователя нет в БД"""
        user_table_name = sql.Identifier(current_app.config['USER_TABLE_NAME'])
        conn = get_conn_to_db()
        cursor = conn.cursor()
        data = [email]
        cursor.execute(sql.SQL("""SELECT * FROM {user_table_name} WHERE
                                  email = %s;""").format(
            user_table_name=user_table_name), data)
        user_data = cursor.fetchone()
        cursor.close()
        close_db_conn()
        user_dict = dict()
        if user_data:
            try:
                user_dict['id'] = user_data[0]
                user_dict['email'] = user_data[1]
                user_dict['password'] = user_data[2]
                user_dict['is_admin'] = user_data[3]
                user_dict['registration_date'] = user_data[4]
            except IndexError:
                return user_dict
        return user_dict

    @staticmethod
    def get_user_dict_by_id(user_id):
        """Метод принимает user_id пользователя.
        Возвращает данные пользователя или None, если такого пользователя нет в БД"""
        user_table_name = sql.Identifier(current_app.config['USER_TABLE_NAME'])
        conn = get_conn_to_db()
        cursor = conn.cursor()
        data = [user_id]
        cursor.execute(sql.SQL("""SELECT * FROM {user_table_name} WHERE
                                      id = %s;""").format(
            user_table_name=user_table_name), data)
        user_data = cursor.fetchone()
        cursor.close()
        close_db_conn()
        user_dict = dict()
        if user_data:
            try:
                user_dict['id'] = user_data[0]
                user_dict['email'] = user_data[1]
                user_dict['password'] = user_data[2]
                user_dict['is_admin'] = user_data[3]
                user_dict['registration_date'] = user_data[4]
            except IndexError:
                return user_dict
        return user_dict

    @staticmethod
    def encode_auth_token(user_id):
        """Метод принимает user_id - id пользователя.
        Возвращает его jwt токен"""
        if isinstance(user_id, int):
            try:
                payload = {
                    'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
                    'iat': datetime.utcnow(),
                    'sub': user_id
                }
                return jwt.encode(
                    payload,
                    current_app.config.get('SECRET_KEY'),
                    algorithm='HS256'
                )
            except Exception as e:
                print(e)
        else:
            print('id пользователя должен иметь тип int.')


class BlacklistToken:
    """Класс для хранения методов, связанных с таблицей BlacklistToken"""

    @staticmethod
    def save(token):
        """Метод принимает token. Сохраняет его в БД"""
        blacklist_token_table_name = sql.Identifier(current_app.config['BLACKLIST_TOKEN_TABLE_NAME'])
        conn = get_conn_to_db()
        cursor = conn.cursor()
        blacklisted_date = datetime.utcnow()
        data = [token, blacklisted_date]
        cursor.execute(sql.SQL("""INSERT INTO {blacklist_token_table_name} 
                                  (token, blacklisted_date) 
                                  VALUES(%s, %s);""").format(
            blacklist_token_table_name=blacklist_token_table_name), data)
        conn.commit()
        cursor.close()
        close_db_conn()

    @staticmethod
    def is_token_in_blacklist(token):
        """Метод принимает token. Возвращает True, если токен находится в чёрном списке
        и False в обратном случае."""
        blacklist_token_table_name = sql.Identifier(current_app.config['BLACKLIST_TOKEN_TABLE_NAME'])
        conn = get_conn_to_db()
        cursor = conn.cursor()
        data = [token]
        cursor.execute(sql.SQL("""SELECT token FROM {blacklist_token_table_name}
                                  WHERE token = %s;""").format(
            blacklist_token_table_name=blacklist_token_table_name), data)
        token = cursor.fetchone()
        cursor.close()
        close_db_conn()
        return bool(token)


def decode_auth_token(token):
    """
    Проверяет токен и возвращает субъект токена (id пользователя), если он действительный и не находится в чёрном
    списке. Иначе возвращает сообщения о том, что токен в чёрном списке, либо просроченный, либо неверный.
    """
    try:
        payload = jwt.decode(token, key=current_app.config.get('SECRET_KEY'), algorithms="HS256")
        is_blacklisted_token = BlacklistToken.is_token_in_blacklist(token)
        if is_blacklisted_token:
            return 'Token blacklisted. Please log in again.'
        else:
            return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
