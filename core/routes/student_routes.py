from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime
# Cambiar las importaciones para usar los nuevos módulos
from core.db.student_db import (
    get_all_students, get_student_by_id, create_student, 
    update_student, delete_student
)
from core.db.grade_db import get_all_grades

students_bp = Blueprint('students', __name__, template_folder='../templates')

@students_bp.route('/')
def list_students():
    """Lista todos los estudiantes."""
    try:
        students = get_all_students(current_app.config['DB_CONFIG'])
        return render_template('students/list.html', students=students, title='Lista de Estudiantes')
    except Exception as e:
        flash(f"Error al obtener estudiantes: {str(e)}", "error")
        return render_template('students/list.html', students=[], title='Lista de Estudiantes')

@students_bp.route('/<int:student_id>')
def student_detail(student_id):
    """Muestra los detalles de un estudiante específico."""
    try:
        student = get_student_by_id(current_app.config['DB_CONFIG'], student_id)
        if student:
            # Obtener las asignaturas en las que está inscrito el estudiante
            from core.db.subject_db import get_student_subjects
            enrolled_subjects = get_student_subjects(current_app.config['DB_CONFIG'], student_id)
            return render_template('students/detail.html', student=student, enrolled_subjects=enrolled_subjects, title='Detalles del Estudiante')
        else:
            flash("Estudiante no encontrado.", "error")
            return redirect(url_for('students.list_students'))
    except Exception as e:
        flash(f"Error al obtener detalles del estudiante: {str(e)}", "error")
        return redirect(url_for('students.list_students'))

@students_bp.route('/new', methods=['GET', 'POST'])
def new_student():
    """Crea un nuevo estudiante."""
    if request.method == 'POST':
        try:
            # Convertir la fecha de nacimiento de string a date object si existe
            birth_date = None
            if request.form.get('birth_date'):
                birth_date = datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date()
            
            # Recopilamos datos del formulario
            student_data = {
                'grade_id': request.form.get('grade_id'),
                'id_type': request.form.get('id_type'),
                'id_number': request.form.get('id_number'),
                'first_name': request.form.get('first_name'),
                'last_name': request.form.get('last_name'),
                'birth_date': birth_date,
                'residence_city': request.form.get('residence_city'),
                'address': request.form.get('address'),
                'email': request.form.get('email'),
                'phone_landline': request.form.get('phone_landline'),
                'phone_mobile': request.form.get('phone_mobile'),
                'guardian_full_name': request.form.get('guardian_full_name')
            }
            
            # Crear el estudiante en la base de datos
            student_id = create_student(current_app.config['DB_CONFIG'], student_data)
            
            if student_id:
                flash("Estudiante creado exitosamente.", "success")
                return redirect(url_for('students.student_detail', student_id=student_id))
            else:
                flash("Error al crear estudiante.", "error")
                grades = get_all_grades(current_app.config['DB_CONFIG'])
                return render_template('students/form.html', student=student_data, grades=grades, title='Nuevo Estudiante')
        
        except Exception as e:
            flash(f"Error al crear estudiante: {str(e)}", "error")
            grades = get_all_grades(current_app.config['DB_CONFIG'])
            return render_template('students/form.html', student=request.form, grades=grades, title='Nuevo Estudiante')
    
    else:  # GET request
        grades = get_all_grades(current_app.config['DB_CONFIG'])
        return render_template('students/form.html', student=None, grades=grades, title='Nuevo Estudiante')

@students_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    """Edita un estudiante existente."""
    if request.method == 'POST':
        try:
            # Convertir la fecha de nacimiento de string a date object si existe
            birth_date = None
            if request.form.get('birth_date'):
                birth_date = datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date()
            
            # Recopilamos datos del formulario
            student_data = {
                'grade_id': request.form.get('grade_id'),
                'id_type': request.form.get('id_type'),
                'id_number': request.form.get('id_number'),
                'first_name': request.form.get('first_name'),
                'last_name': request.form.get('last_name'),
                'birth_date': birth_date,
                'residence_city': request.form.get('residence_city'),
                'address': request.form.get('address'),
                'email': request.form.get('email'),
                'phone_landline': request.form.get('phone_landline'),
                'phone_mobile': request.form.get('phone_mobile'),
                'guardian_full_name': request.form.get('guardian_full_name')
            }
            
            # Actualizar el estudiante en la base de datos
            success = update_student(current_app.config['DB_CONFIG'], student_id, student_data)
            
            if success:
                flash("Estudiante actualizado exitosamente.", "success")
                return redirect(url_for('students.student_detail', student_id=student_id))
            else:
                flash("Error al actualizar estudiante.", "error")
                grades = get_all_grades(current_app.config['DB_CONFIG'])
                return render_template('students/form.html', student=student_data, student_id=student_id, grades=grades, title='Editar Estudiante')
        
        except Exception as e:
            flash(f"Error al actualizar estudiante: {str(e)}", "error")
            grades = get_all_grades(current_app.config['DB_CONFIG'])
            return render_template('students/form.html', student=request.form, student_id=student_id, grades=grades, title='Editar Estudiante')
    
    else:  # GET request
        try:
            student = get_student_by_id(current_app.config['DB_CONFIG'], student_id)
            if student:
                grades = get_all_grades(current_app.config['DB_CONFIG'])
                return render_template('students/form.html', student=student, student_id=student_id, grades=grades, title='Editar Estudiante')
            else:
                flash("Estudiante no encontrado.", "error")
                return redirect(url_for('students.list_students'))
        except Exception as e:
            flash(f"Error al obtener datos del estudiante: {str(e)}", "error")
            return redirect(url_for('students.list_students'))

@students_bp.route('/<int:student_id>/delete', methods=['POST'])
def delete_student_route(student_id):
    """Elimina un estudiante."""
    try:
        # Primero obtenemos el estudiante para verificar que existe
        student = get_student_by_id(current_app.config['DB_CONFIG'], student_id)
        
        if not student:
            flash("Estudiante no encontrado.", "error")
            return redirect(url_for('students.list_students'))
        
        # Intentamos eliminar el estudiante
        success = delete_student(current_app.config['DB_CONFIG'], student_id)
        
        if success:
            flash("Estudiante eliminado exitosamente.", "success")
        else:
            flash("Error al eliminar estudiante.", "error")
        
        return redirect(url_for('students.list_students'))
    
    except Exception as e:
        flash(f"Error al eliminar estudiante: {str(e)}", "error")
        return redirect(url_for('students.list_students'))