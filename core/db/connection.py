import mysql.connector
from mysql.connector import Error

def get_db_connection(db_config):
    """Crea y retorna una conexión a la base de datos y un cursor."""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        return conn, cursor
    except Error as e:
        print(f"Error al conectar a MySQL como usuario '{db_config.get('user')}': {e}")
        return None, None

def close_connection(conn, cursor):
    """Cierra el cursor y la conexión a la base de datos."""
    if cursor:
        cursor.close()
    if conn and conn.is_connected():
        conn.close()
