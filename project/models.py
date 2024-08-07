from db import get_conn_to_db, close_db_conn, USER_TABLE_NAME
from psycopg2 import sql
from datetime import datetime


def save_user(email, password):
    conn = get_conn_to_db()
    cursor = conn.cursor()
    data = [email, password]
    cursor.execute(sql.SQL("""INSERT INTO {user_table_name} 
                              (email, password) 
                              VALUES(%s, %s);""").format(
        user_table_name=USER_TABLE_NAME), data)
    conn.commit()
    cursor.close()
    close_db_conn()
    