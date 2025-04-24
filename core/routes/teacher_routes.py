from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime
from core.db.teacher_db import (
    get_all_teachers, get_teacher_by_id, create_teacher,
    update_teacher, delete_teacher, get_teacher_subjects, get_teacher_grades
)

teachers_bp = Blueprint('teachers', __name__, template_folder='../templates')

@teachers_bp.route('/')
def list_teachers():
    try:
        teachers = get_all_teachers(current_app.config['DB_CONFIG'])
        return render_template('teachers/list.html', teachers=teachers, title='Lista de Docentes')
    except Exception as e:
        flash(f"Error al obtener docentes: {str(e)}", "error")
        return render_template('teachers/list.html', teachers=[], title='Lista de Docentes')

@teachers_bp.route('/<int:teacher_id>')
def teacher_detail(teacher_id):
    try:
        teacher = get_teacher_by_id(current_app.config['DB_CONFIG'], teacher_id)
        if teacher:
            subjects = get_teacher_subjects(current_app.config['DB_CONFIG'], teacher_id)
            grades = get_teacher_grades(current_app.config['DB_CONFIG'], teacher_id)
            return render_template('teachers/detail.html',
                teacher=teacher,
                subjects=subjects,
                grades=grades,
                title='Detalles del Docente')
        else:
            flash("Docente no encontrado.", "error")
            return redirect(url_for('teachers.list_teachers'))
    except Exception as e:
        flash(f"Error al obtener detalles del docente: {str(e)}", "error")
        return redirect(url_for('teachers.list_teachers'))

@teachers_bp.route('/new', methods=['GET', 'POST'])
def new_teacher():
    if request.method == 'POST':
        try:
            birth_date = None
            if request.form.get('birth_date'):
                birth_date = datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date()
            teacher_data = {
                'id_type': request.form.get('id_type'),
                'id_number': request.form.get('id_number'),
                'first_name': request.form.get('first_name'),
                'last_name': request.form.get('last_name'),
                'birth_date': birth_date,
                'education_level': request.form.get('education_level'),
                'email': request.form.get('email'),
                'phone_landline': request.form.get('phone_landline'),
                'phone_mobile': request.form.get('phone_mobile')
            }
            teacher_id = create_teacher(current_app.config['DB_CONFIG'], teacher_data)
            if teacher_id:
                flash("Docente creado exitosamente.", "success")
                return redirect(url_for('teachers.teacher_detail', teacher_id=teacher_id))
            else:
                flash("Error al crear docente.", "error")
                return render_template('teachers/form.html', teacher=teacher_data, title='Nuevo Docente')
        except Exception as e:
            flash(f"Error al crear docente: {str(e)}", "error")
            return render_template('teachers/form.html', teacher=request.form, title='Nuevo Docente')
    else:
        return render_template('teachers/form.html', teacher=None, title='Nuevo Docente')

@teachers_bp.route('/<int:teacher_id>/edit', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    if request.method == 'POST':
        try:
            birth_date = None
            if request.form.get('birth_date'):
                birth_date = datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date()
            teacher_data = {
                'id_type': request.form.get('id_type'),
                'id_number': request.form.get('id_number'),
                'first_name': request.form.get('first_name'),
                'last_name': request.form.get('last_name'),
                'birth_date': birth_date,
                'education_level': request.form.get('education_level'),
                'email': request.form.get('email'),
                'phone_landline': request.form.get('phone_landline'),
                'phone_mobile': request.form.get('phone_mobile')
            }
            success = update_teacher(current_app.config['DB_CONFIG'], teacher_id, teacher_data)
            if success:
                flash("Docente actualizado exitosamente.", "success")
                return redirect(url_for('teachers.teacher_detail', teacher_id=teacher_id))
            else:
                flash("Error al actualizar docente.", "error")
                return render_template('teachers/form.html', teacher=teacher_data, teacher_id=teacher_id, title='Editar Docente')
        except Exception as e:
            flash(f"Error al actualizar docente: {str(e)}", "error")
            return render_template('teachers/form.html', teacher=request.form, teacher_id=teacher_id, title='Editar Docente')
    else:
        try:
            teacher = get_teacher_by_id(current_app.config['DB_CONFIG'], teacher_id)
            if teacher:
                return render_template('teachers/form.html', teacher=teacher, teacher_id=teacher_id, title='Editar Docente')
            else:
                flash("Docente no encontrado.", "error")
                return redirect(url_for('teachers.list_teachers'))
        except Exception as e:
            flash(f"Error al obtener datos del docente: {str(e)}", "error")
            return redirect(url_for('teachers.list_teachers'))

@teachers_bp.route('/<int:teacher_id>/delete', methods=['POST'])
def delete_teacher_route(teacher_id):
    try:
        teacher = get_teacher_by_id(current_app.config['DB_CONFIG'], teacher_id)
        if not teacher:
            flash("Docente no encontrado.", "error")
            return redirect(url_for('teachers.list_teachers'))
        success = delete_teacher(current_app.config['DB_CONFIG'], teacher_id)
        if success:
            flash("Docente eliminado exitosamente.", "success")
        else:
            flash("Error al eliminar docente.", "error")
        return redirect(url_for('teachers.list_teachers'))
    except Exception as e:
        flash(f"Error al eliminar docente: {str(e)}", "error")
        return redirect(url_for('teachers.list_teachers'))