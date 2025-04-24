from mysql.connector import Error
from .connection import get_db_connection, close_connection

def get_all_students(db_config):
    """Obtiene todos los estudiantes de la base de datos."""
    conn, cursor = get_db_connection(db_config)
    students = []
    
    try:
        if conn and cursor:
            cursor.execute("""
                SELECT s.*, g.grade_name 
                FROM students s 
                LEFT JOIN grades g ON s.grade_id = g.grade_id 
                ORDER BY s.last_name
            """)
            students = cursor.fetchall()
    except Error as e:
        print(f"Error en get_all_students: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return students

def get_student_by_id(db_config, student_id):
    """Obtiene un estudiante por su ID."""
    conn, cursor = get_db_connection(db_config)
    student = None
    
    try:
        if conn and cursor:
            cursor.execute("""
                SELECT s.*, g.grade_name 
                FROM students s 
                LEFT JOIN grades g ON s.grade_id = g.grade_id 
                WHERE s.student_id = %s
            """, (student_id,))
            student = cursor.fetchone()
    except Error as e:
        print(f"Error en get_student_by_id: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return student

def create_student(db_config, student_data):
    """Crea un nuevo estudiante en la base de datos."""
    conn, cursor = get_db_connection(db_config)
    
    try:
        if conn and cursor:
            # Preparar consulta SQL con los campos específicos
            cursor.execute("""
                INSERT INTO students (
                    grade_id, id_type, id_number, first_name, last_name, 
                    birth_date, residence_city, address, email, 
                    phone_landline, phone_mobile, guardian_full_name
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                student_data.get('grade_id'),
                student_data.get('id_type'),
                student_data.get('id_number'),
                student_data.get('first_name'),
                student_data.get('last_name'),
                student_data.get('birth_date'),
                student_data.get('residence_city'),
                student_data.get('address'),
                student_data.get('email'),
                student_data.get('phone_landline'),
                student_data.get('phone_mobile'),
                student_data.get('guardian_full_name')
            ))
            conn.commit()
            return cursor.lastrowid
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error en create_student: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return None

def update_student(db_config, student_id, student_data):
    """Actualiza un estudiante existente en la base de datos."""
    conn, cursor = get_db_connection(db_config)
    
    try:
        if conn and cursor:
            cursor.execute("""
                UPDATE students SET 
                    grade_id = %s,
                    id_type = %s,
                    id_number = %s,
                    first_name = %s,
                    last_name = %s,
                    birth_date = %s,
                    residence_city = %s,
                    address = %s,
                    email = %s,
                    phone_landline = %s,
                    phone_mobile = %s,
                    guardian_full_name = %s
                WHERE student_id = %s
            """, (
                student_data.get('grade_id'),
                student_data.get('id_type'),
                student_data.get('id_number'),
                student_data.get('first_name'),
                student_data.get('last_name'),
                student_data.get('birth_date'),
                student_data.get('residence_city'),
                student_data.get('address'),
                student_data.get('email'),
                student_data.get('phone_landline'),
                student_data.get('phone_mobile'),
                student_data.get('guardian_full_name'),
                student_id
            ))
            conn.commit()
            return cursor.rowcount > 0
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error en update_student: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return False

def delete_student(db_config, student_id):
    """Elimina un estudiante de la base de datos."""
    conn, cursor = get_db_connection(db_config)
    
    try:
        if conn and cursor:
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            conn.commit()
            return cursor.rowcount > 0
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error en delete_student: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return False
