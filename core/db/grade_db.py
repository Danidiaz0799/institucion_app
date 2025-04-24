from mysql.connector import Error
from .connection import get_db_connection, close_connection

def get_all_grades(db_config):
    conn, cursor = get_db_connection(db_config)
    grades = []
    try:
        if conn and cursor:
            cursor.execute("""
                SELECT g.grade_id, g.grade_name, g.director_teacher_id,
                    t.first_name AS teacher_first_name, t.last_name AS teacher_last_name
                FROM grades g
                LEFT JOIN teachers t ON g.director_teacher_id = t.teacher_id
                ORDER BY g.grade_name
            """)
            grades = cursor.fetchall()
    except Error as e:
        print(f"Error en get_all_grades: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    return grades

def get_grade_by_id(db_config, grade_id):
    conn, cursor = get_db_connection(db_config)
    grade = None
    try:
        if conn and cursor:
            cursor.execute("""
                SELECT g.grade_id, g.grade_name, g.director_teacher_id,
                    t.first_name AS teacher_first_name, t.last_name AS teacher_last_name
                FROM grades g
                LEFT JOIN teachers t ON g.director_teacher_id = t.teacher_id
                WHERE g.grade_id = %s
            """, (grade_id,))
            grade = cursor.fetchone()
    except Error as e:
        print(f"Error en get_grade_by_id: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    return grade

def create_grade(db_config, grade_data):
    conn, cursor = get_db_connection(db_config)
    grade_id = None
    try:
        if conn and cursor:
            director_teacher_id = grade_data.get('director_teacher_id')
            if not director_teacher_id:
                director_teacher_id = None
            cursor.execute(
                "INSERT INTO grades (grade_name, director_teacher_id) VALUES (%s, %s)",
                (grade_data.get('grade_name'), director_teacher_id)
            )
            conn.commit()
            grade_id = cursor.lastrowid
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error en create_grade: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    return grade_id

def update_grade(db_config, grade_id, grade_data):
    conn, cursor = get_db_connection(db_config)
    success = False
    try:
        if conn and cursor:
            director_teacher_id = grade_data.get('director_teacher_id')
            if not director_teacher_id:
                director_teacher_id = None
            cursor.execute(
                "UPDATE grades SET grade_name = %s, director_teacher_id = %s WHERE grade_id = %s",
                (grade_data.get('grade_name'), director_teacher_id, grade_id)
            )
            conn.commit()
            success = cursor.rowcount > 0
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error en update_grade: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    return success

def delete_grade(db_config, grade_id):
    conn, cursor = get_db_connection(db_config)
    success = False
    try:
        if conn and cursor:
            cursor.execute("SELECT COUNT(*) AS count FROM students WHERE grade_id = %s", (grade_id,))
            result = cursor.fetchone()
            if result and result['count'] > 0:
                return False
            cursor.execute("DELETE FROM grades WHERE grade_id = %s", (grade_id,))
            conn.commit()
            success = cursor.rowcount > 0
    except Error as e:
        if conn:
            conn.rollback()
        print(f"Error en delete_grade: {e}")
        raise e
    finally:
        close_connection(conn, cursor)
    return success

def get_grade_students(db_config, grade_id):
    conn, cursor = get_db_connection(db_config)
    students = []
    try:
        if conn and cursor:
            cursor.execute("""
                SELECT student_id, first_name, last_name, email
                FROM students
                WHERE grade_id = %s
                ORDER BY last_name, first_name
            """, (grade_id,))
            students = cursor.fetchall()
    except Error as e:
        print(f"Error en get_grade_students: {e}")
        raise e
    finally:
        close_connection(conn, cursor)

    return students
