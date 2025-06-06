from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from core.db.subject_db import (
    get_all_subjects, get_subject_by_id, create_subject, update_subject, delete_subject,
    get_subject_students, get_students_not_in_subject,
    assign_student_to_subject, remove_student_from_subject
)
from core.db.teacher_db import get_all_teachers

subjects_bp = Blueprint('subjects', __name__, template_folder='../templates')

@subjects_bp.route('/')
def list_subjects():
    try:
        subjects = get_all_subjects(current_app.config['DB_CONFIG'])
        return render_template('subjects/subjects_list.html', subjects=subjects, title='Lista de Asignaturas')
    except Exception as e:
        flash(f"Error al obtener asignaturas: {str(e)}", "error")
        return render_template('subjects/subjects_list.html', subjects=[], title='Lista de Asignaturas')

@subjects_bp.route('/new', methods=['GET', 'POST'])
def new_subject():
    if request.method == 'POST':
        try:
            subject_name = request.form.get('subject_name')
            teacher_id = request.form.get('teacher_id') or None
            if not subject_name:
                flash("El nombre de la asignatura es obligatorio", "error")
                teachers = get_all_teachers(current_app.config['DB_CONFIG'])
                return render_template('subjects/subject_form.html', teachers=teachers, title='Nueva Asignatura')
            subject_id = create_subject(current_app.config['DB_CONFIG'], subject_name, teacher_id)
            if subject_id:
                flash("Asignatura creada exitosamente", "success")
                return redirect(url_for('subjects.list_subjects'))
            else:
                flash("Error al crear asignatura", "error")
                teachers = get_all_teachers(current_app.config['DB_CONFIG'])
                return render_template('subjects/subject_form.html', teachers=teachers, title='Nueva Asignatura')
        except Exception as e:
            flash(f"Error al crear asignatura: {str(e)}", "error")
            teachers = get_all_teachers(current_app.config['DB_CONFIG'])
            return render_template('subjects/subject_form.html', teachers=teachers, title='Nueva Asignatura')
    else:
        teachers = get_all_teachers(current_app.config['DB_CONFIG'])
        return render_template('subjects/subject_form.html', teachers=teachers, subject=None, title='Nueva Asignatura')

@subjects_bp.route('/<int:subject_id>/edit', methods=['GET', 'POST'])
def edit_subject(subject_id):
    if request.method == 'POST':
        try:
            subject_name = request.form.get('subject_name')
            teacher_id = request.form.get('teacher_id') or None
            if not subject_name:
                flash("El nombre de la asignatura es obligatorio", "error")
                teachers = get_all_teachers(current_app.config['DB_CONFIG'])
                subject = get_subject_by_id(current_app.config['DB_CONFIG'], subject_id)
                return render_template('subjects/subject_form.html', subject=subject, teachers=teachers, title='Editar Asignatura')
            success = update_subject(current_app.config['DB_CONFIG'], subject_id, subject_name, teacher_id)
            if success:
                flash("Asignatura actualizada exitosamente", "success")
                return redirect(url_for('subjects.list_subjects'))
            else:
                flash("Error al actualizar asignatura", "error")
                teachers = get_all_teachers(current_app.config['DB_CONFIG'])
                subject = get_subject_by_id(current_app.config['DB_CONFIG'], subject_id)
                return render_template('subjects/subject_form.html', subject=subject, teachers=teachers, title='Editar Asignatura')
        except Exception as e:
            flash(f"Error al actualizar asignatura: {str(e)}", "error")
            teachers = get_all_teachers(current_app.config['DB_CONFIG'])
            subject = get_subject_by_id(current_app.config['DB_CONFIG'], subject_id)
            return render_template('subjects/subject_form.html', subject=subject, teachers=teachers, title='Editar Asignatura')
    else:
        try:
            subject = get_subject_by_id(current_app.config['DB_CONFIG'], subject_id)
            if subject:
                teachers = get_all_teachers(current_app.config['DB_CONFIG'])
                return render_template('subjects/subject_form.html', subject=subject, teachers=teachers, title='Editar Asignatura')
            else:
                flash("Asignatura no encontrada", "error")
                return redirect(url_for('subjects.list_subjects'))
        except Exception as e:
            flash(f"Error al obtener datos de la asignatura: {str(e)}", "error")
            return redirect(url_for('subjects.list_subjects'))

@subjects_bp.route('/<int:subject_id>/delete', methods=['POST'])
def delete_subject_post(subject_id):
    try:
        success = delete_subject(current_app.config['DB_CONFIG'], subject_id)
        if success:
            flash("Asignatura eliminada exitosamente", "success")
        else:
            flash("Error al eliminar asignatura", "error")
        return redirect(url_for('subjects.list_subjects'))
    except Exception as e:
        flash(f"Error al eliminar asignatura: {str(e)}", "error")
        return redirect(url_for('subjects.list_subjects'))

# --- Rutas para gestionar estudiantes en asignaturas ---

@subjects_bp.route('/<int:subject_id>/manage', methods=['GET', 'POST'])
def manage_subject_students(subject_id):
    try:
        subject = get_subject_by_id(current_app.config['DB_CONFIG'], subject_id)
        if not subject:
            flash("Asignatura no encontrada", "error")
            return redirect(url_for('subjects.list_subjects'))
        if request.method == 'POST':
            if 'add_student' in request.form:
                student_id_to_add = request.form.get('add_student')
                if student_id_to_add:
                    try:
                        success = assign_student_to_subject(current_app.config['DB_CONFIG'], student_id_to_add, subject_id)
                        if success:
                            flash("Estudiante inscrito exitosamente", "success")
                        else:
                            flash("Error al inscribir estudiante", "error")
                    except Exception as e:
                        flash(f"Error al inscribir: {str(e)}", "error")
                else:
                    flash("No se seleccionó ningún estudiante para añadir.", "warning")
            elif 'remove_student' in request.form:
                student_id_to_remove = request.form.get('remove_student')
                if student_id_to_remove:
                    try:
                        success = remove_student_from_subject(current_app.config['DB_CONFIG'], student_id_to_remove, subject_id)
                        if success:
                            flash("Inscripción de estudiante eliminada exitosamente", "success")
                        else:
                            flash("Error al eliminar inscripción", "error")
                    except Exception as e:
                        flash(f"Error al eliminar inscripción: {str(e)}", "error")
            return redirect(url_for('subjects.manage_subject_students', subject_id=subject_id))
        enrolled_students = get_subject_students(current_app.config['DB_CONFIG'], subject_id)
        available_students = get_students_not_in_subject(current_app.config['DB_CONFIG'], subject_id)
        return render_template('subjects/manage_students.html',
            subject=subject,
            enrolled_students=enrolled_students,
            available_students=available_students,
            title=f"Gestionar Estudiantes - {subject['subject_name']}")
    except Exception as e:
        flash(f"Error al obtener datos para gestionar estudiantes: {str(e)}", "error")
        return redirect(url_for('subjects.list_subjects'))