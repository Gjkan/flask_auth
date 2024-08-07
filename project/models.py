from db import get_conn_to_db, close_db_conn, USER_TABLE_NAME, BLACKLIST_TOKEN_TABLE_NAME
from psycopg2 import sql
from datetime import datetime


def save_user(email, password):
    conn = get_conn_to_db()
    cursor = conn.cursor()
    registration_date = datetime.now()
    data = [email, password, registration_date]
    cursor.execute(sql.SQL("""INSERT INTO {user_table_name} 
                              (email, password, registration_date)
                              VALUES(%s, %s, %s);""").format(
        user_table_name=USER_TABLE_NAME), data)
    conn.commit()
    cursor.close()
    close_db_conn()
   

def save_token(token, is_blacklisted=False):
    conn = get_conn_to_db()
    cursor = conn.cursor()
    data = [token, is_blacklisted]
    cursor.execute(sql.SQL("""INSERT INTO {blacklist_token_table_name} 
                              (token, is_blacklisted) 
                              VALUES(%s, %s);""").format(
        blacklist_token_table_name=BLACKLIST_TOKEN_TABLE_NAME), data)
    conn.commit()
    cursor.close()
    close_db_conn()
    