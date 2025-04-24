from mysql.connector import Error
from .connection import get_db_connection, close_connection

def get_all_grades(db_config):
    """Obtiene todos los grados para usar en formularios."""
    conn, cursor = get_db_connection(db_config)
    grades = []
    
    try:
        if conn and cursor:
            cursor.execute("SELECT grade_id, grade_name FROM grades ORDER BY grade_name")
            grades = cursor.fetchall()
    except Error as e:
        print(f"Error en get_all_grades: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return grades
