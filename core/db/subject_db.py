from mysql.connector import Error
from .connection import get_db_connection, close_connection

def get_all_subjects(db_config):
    conn, cursor = get_db_connection(db_config)
    subjects = []
    if not conn:
        return subjects
    try:
        query = """
        SELECT s.subject_id, s.subject_name, s.teacher_id,
            t.first_name AS teacher_first_name, t.last_name AS teacher_last_name
        FROM subjects s
        LEFT JOIN teachers t ON s.teacher_id = t.teacher_id
        ORDER BY s.subject_name
        """
        cursor.execute(query)
        subjects = cursor.fetchall()
    except Error as e:
        print(f"Error en get_all_subjects: {e}")
    finally:
        close_connection(conn, cursor)
    return subjects

def get_subject_by_id(db_config, subject_id):
    conn, cursor = get_db_connection(db_config)
    subject = None
    if not conn:
        return subject
    try:
        query = """
        SELECT s.subject_id, s.subject_name, s.teacher_id,
            t.first_name AS teacher_first_name, t.last_name AS teacher_last_name
        FROM subjects s
        LEFT JOIN teachers t ON s.teacher_id = t.teacher_id
        WHERE s.subject_id = %s
        """
        cursor.execute(query, (subject_id,))
        subject = cursor.fetchone()
    except Error as e:
        print(f"Error en get_subject_by_id: {e}")
    finally:
        close_connection(conn, cursor)
    return subject

def create_subject(db_config, subject_name, teacher_id):
    conn, cursor = get_db_connection(db_config)
    subject_id = None
    if not conn:
        return subject_id
    try:
        teacher_id_to_insert = teacher_id if teacher_id else None
        cursor.execute(
            "INSERT INTO subjects (subject_name, teacher_id) VALUES (%s, %s)",
            (subject_name, teacher_id_to_insert)
        )
        conn.commit()
        subject_id = cursor.lastrowid
    except Error as e:
        print(f"Error en create_subject: {e}")
        if conn:
            conn.rollback()
    finally:
        close_connection(conn, cursor)
    return subject_id

def update_subject(db_config, subject_id, subject_name, teacher_id):
    conn, cursor = get_db_connection(db_config)
    success = False
    if not conn:
        return success
    try:
        teacher_id_to_update = teacher_id if teacher_id else None
        cursor.execute(
            "UPDATE subjects SET subject_name = %s, teacher_id = %s WHERE subject_id = %s",
            (subject_name, teacher_id_to_update, subject_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
    except Error as e:
        print(f"Error en update_subject: {e}")
        if conn:
            conn.rollback()
    finally:
        close_connection(conn, cursor)
    return success

def delete_subject(db_config, subject_id):
    conn, cursor = get_db_connection(db_config)
    success = False
    if not conn:
        return success
    try:
        try:
            cursor.execute("DELETE FROM student_subjects WHERE subject_id = %s", (subject_id,))
        except Error as e:
            print(f"Error al eliminar inscripciones de estudiantes (puede ser normal si no hay): {e}")
        cursor.execute("DELETE FROM subjects WHERE subject_id = %s", (subject_id,))
        conn.commit()
        success = cursor.rowcount > 0
    except Error as e:
        print(f"Error en delete_subject: {e}")
        if conn:
            conn.rollback()
    finally:
        close_connection(conn, cursor)
    return success

# --- Funciones para gestionar estudiantes en asignaturas ---

def get_subject_students(db_config, subject_id):
    conn, cursor = get_db_connection(db_config)
    students = []
    if not conn:
        return students
    try:
        query = """
        SELECT s.student_id, s.first_name, s.last_name, s.email, g.grade_name
        FROM students s
        JOIN student_subjects ss ON s.student_id = ss.student_id
        LEFT JOIN grades g ON s.grade_id = g.grade_id
        WHERE ss.subject_id = %s
        ORDER BY s.last_name, s.first_name
        """
        cursor.execute(query, (subject_id,))
        students = cursor.fetchall()
    except Error as e:
        print(f"Error en get_subject_students: {e}")
    finally:
        close_connection(conn, cursor)
    return students

def get_students_not_in_subject(db_config, subject_id):
    conn, cursor = get_db_connection(db_config)
    students = []
    if not conn:
        return students
    try:
        query = """
        SELECT s.student_id, s.first_name, s.last_name, g.grade_name
        FROM students s
        LEFT JOIN grades g ON s.grade_id = g.grade_id
        WHERE s.student_id NOT IN (
            SELECT ss.student_id
            FROM student_subjects ss
            WHERE ss.subject_id = %s
        )
        ORDER BY s.last_name, s.first_name
        """
        cursor.execute(query, (subject_id,))
        students = cursor.fetchall()
    except Error as e:
        print(f"Error en get_students_not_in_subject: {e}")
    finally:
        close_connection(conn, cursor)
    return students

def assign_student_to_subject(db_config, student_id, subject_id):
    conn, cursor = get_db_connection(db_config)
    success = False
    if not conn:
        return success
    try:
        cursor.execute(
            "SELECT 1 FROM student_subjects WHERE student_id = %s AND subject_id = %s",
            (student_id, subject_id)
        )
        if cursor.fetchone():
            return True # Ya asignado

        cursor.execute(
            "INSERT INTO student_subjects (student_id, subject_id) VALUES (%s, %s)",
            (student_id, subject_id)
        )
        conn.commit()
        success = True
    except Error as e:
        print(f"Error en assign_student_to_subject: {e}")
        if conn:
            conn.rollback()
    finally:
        close_connection(conn, cursor)
    return success

def remove_student_from_subject(db_config, student_id, subject_id):
    conn, cursor = get_db_connection(db_config)
    success = False
    if not conn:
        return success
    try:
        cursor.execute(
            "DELETE FROM student_subjects WHERE student_id = %s AND subject_id = %s",
            (student_id, subject_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
    except Error as e:
        print(f"Error en remove_student_from_subject: {e}")
        if conn:
            conn.rollback()
    finally:
        close_connection(conn, cursor)
    return success

def get_student_subjects(db_config, student_id):
    conn, cursor = get_db_connection(db_config)
    subjects = []
    if not conn:
        return subjects
    try:
        query = """
        SELECT s.subject_id, s.subject_name,
            t.first_name AS teacher_first_name, t.last_name AS teacher_last_name
        FROM subjects s
        JOIN student_subjects ss ON s.subject_id = ss.subject_id
        LEFT JOIN teachers t ON s.teacher_id = t.teacher_id
        WHERE ss.student_id = %s
        ORDER BY s.subject_name
        """
        cursor.execute(query, (student_id,))
        subjects = cursor.fetchall()
    except Error as e:
        print(f"Error en get_student_subjects: {e}")
    finally:
        close_connection(conn, cursor)
    return subjects
