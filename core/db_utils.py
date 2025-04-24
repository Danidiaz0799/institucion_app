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
            cursor.execute("""
                SELECT s.* 
                FROM subjects s
                JOIN subject_teacher st ON s.subject_id = st.subject_id
                WHERE st.teacher_id = %s
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