from mysql.connector import Error
from .connection import get_db_connection, close_connection

def get_all_teachers(db_config):
    """Obtiene todos los profesores de la base de datos."""
    conn, cursor = get_db_connection(db_config)
    teachers = []
    
    try:
        if conn and cursor:
            cursor.execute("""
                SELECT * FROM teachers
                ORDER BY last_name
            """)
            teachers = cursor.fetchall()
    except Error as e:
        print(f"Error en get_all_teachers: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return teachers

def get_teacher_by_id(db_config, teacher_id):
    """Obtiene un profesor por su ID."""
    conn, cursor = get_db_connection(db_config)
    teacher = None
    
    try:
        if conn and cursor:
            cursor.execute("SELECT * FROM teachers WHERE teacher_id = %s", (teacher_id,))
            teacher = cursor.fetchone()
    except Error as e:
        print(f"Error en get_teacher_by_id: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return teacher

def create_teacher(db_config, teacher_data):
    """Crea un nuevo profesor en la base de datos."""
    conn, cursor = get_db_connection(db_config)
    
    try:
        if conn and cursor:
            cursor.execute("""
                INSERT INTO teachers (
                    id_type, id_number, first_name, last_name, 
                    birth_date, education_level, email, 
                    phone_landline, phone_mobile
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                teacher_data.get('id_type'),
                teacher_data.get('id_number'),
                teacher_data.get('first_name'),
                teacher_data.get('last_name'),
                teacher_data.get('birth_date'),
                teacher_data.get('education_level'),
                teacher_data.get('email'),
                teacher_data.get('phone_landline'),
                teacher_data.get('phone_mobile')
            ))
            conn.commit()
            return cursor.lastrowid
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error en create_teacher: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return None

def update_teacher(db_config, teacher_id, teacher_data):
    """Actualiza un profesor existente en la base de datos."""
    conn, cursor = get_db_connection(db_config)
    
    try:
        if conn and cursor:
            cursor.execute("""
                UPDATE teachers SET 
                    id_type = %s,
                    id_number = %s,
                    first_name = %s,
                    last_name = %s,
                    birth_date = %s,
                    education_level = %s,
                    email = %s,
                    phone_landline = %s,
                    phone_mobile = %s
                WHERE teacher_id = %s
            """, (
                teacher_data.get('id_type'),
                teacher_data.get('id_number'),
                teacher_data.get('first_name'),
                teacher_data.get('last_name'),
                teacher_data.get('birth_date'),
                teacher_data.get('education_level'),
                teacher_data.get('email'),
                teacher_data.get('phone_landline'),
                teacher_data.get('phone_mobile'),
                teacher_id
            ))
            conn.commit()
            return cursor.rowcount > 0
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error en update_teacher: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return False

def delete_teacher(db_config, teacher_id):
    """Elimina un profesor de la base de datos."""
    conn, cursor = get_db_connection(db_config)
    
    try:
        if conn and cursor:
            cursor.execute("DELETE FROM teachers WHERE teacher_id = %s", (teacher_id,))
            conn.commit()
            return cursor.rowcount > 0
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error en delete_teacher: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return False

def get_teacher_subjects(db_config, teacher_id):
    """Obtiene las asignaturas asignadas a un profesor."""
    conn, cursor = get_db_connection(db_config)
    subjects = []
    
    try:
        if conn and cursor:
            # Corregir la consulta para usar la columna teacher_id en la tabla subjects
            cursor.execute("""
                SELECT s.* 
                FROM subjects s
                WHERE s.teacher_id = %s
                ORDER BY s.subject_name
            """, (teacher_id,))
            subjects = cursor.fetchall()
    except Error as e:
        print(f"Error en get_teacher_subjects: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return subjects

def get_teacher_grades(db_config, teacher_id):
    """Obtiene los grados donde un profesor es director."""
    conn, cursor = get_db_connection(db_config)
    grades = []
    
    try:
        if conn and cursor:
            cursor.execute("""
                SELECT g.* 
                FROM grades g
                WHERE g.director_teacher_id = %s
                ORDER BY g.grade_name
            """, (teacher_id,))
            grades = cursor.fetchall()
    except Error as e:
        print(f"Error en get_teacher_grades: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    
    return grades
