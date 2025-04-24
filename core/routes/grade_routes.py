from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from core.db.grade_db import (
    get_all_grades, get_grade_by_id, create_grade, 
    update_grade, delete_grade, get_grade_students
)
from core.db.teacher_db import get_all_teachers

grades_bp = Blueprint('grades', __name__, template_folder='../templates')

@grades_bp.route('/')
def list_grades():
    """Lista todos los grados."""
    try:
        grades = get_all_grades(current_app.config['DB_CONFIG'])
        return render_template('grades/grades_list.html', grades=grades, title='Lista de Grados')
    except Exception as e:
        flash(f"Error al obtener grados: {str(e)}", "error")
        return render_template('grades/grades_list.html', grades=[], title='Lista de Grados')

@grades_bp.route('/<int:grade_id>')
def grade_detail(grade_id):
    """Muestra detalles de un grado específico, incluyendo sus estudiantes."""
    try:
        grade = get_grade_by_id(current_app.config['DB_CONFIG'], grade_id)
        if grade:
            students = get_grade_students(current_app.config['DB_CONFIG'], grade_id)
            return render_template('grades/grade_detail.html', 
                                  grade=grade, 
                                  students=students,
                                  title=f'Detalles del Grado: {grade["grade_name"]}')
        else:
            flash("Grado no encontrado", "error")
            return redirect(url_for('grades.list_grades'))
    except Exception as e:
        flash(f"Error al obtener detalles del grado: {str(e)}", "error")
        return redirect(url_for('grades.list_grades'))

@grades_bp.route('/new', methods=['GET', 'POST'])
def new_grade():
    """Crea un nuevo grado."""
    if request.method == 'POST':
        try:
            grade_name = request.form.get('grade_name')
            director_teacher_id = request.form.get('director_teacher_id') or None
            
            if not grade_name:
                flash("El nombre del grado es obligatorio", "error")
                teachers = get_all_teachers(current_app.config['DB_CONFIG'])
                return render_template('grades/grade_form.html', title='Nuevo Grado', teachers=teachers)
                
            grade_data = {
                'grade_name': grade_name,
                'director_teacher_id': director_teacher_id
            }
            
            grade_id = create_grade(current_app.config['DB_CONFIG'], grade_data)
            
            if grade_id:
                flash("Grado creado exitosamente", "success")
                return redirect(url_for('grades.list_grades'))
            else:
                flash("Error al crear grado", "error")
                teachers = get_all_teachers(current_app.config['DB_CONFIG'])
                return render_template('grades/grade_form.html', title='Nuevo Grado', teachers=teachers)
        
        except Exception as e:
            flash(f"Error al crear grado: {str(e)}", "error")
            teachers = get_all_teachers(current_app.config['DB_CONFIG'])
            return render_template('grades/grade_form.html', title='Nuevo Grado', teachers=teachers)
    
    else:  # GET request
        teachers = get_all_teachers(current_app.config['DB_CONFIG'])
        return render_template('grades/grade_form.html', grade=None, teachers=teachers, title='Nuevo Grado')

@grades_bp.route('/<int:grade_id>/edit', methods=['GET', 'POST'])
def edit_grade(grade_id):
    """Edita un grado existente."""
    if request.method == 'POST':
        try:
            grade_name = request.form.get('grade_name')
            director_teacher_id = request.form.get('director_teacher_id') or None
            
            if not grade_name:
                flash("El nombre del grado es obligatorio", "error")
                teachers = get_all_teachers(current_app.config['DB_CONFIG'])
                grade = get_grade_by_id(current_app.config['DB_CONFIG'], grade_id)
                return render_template('grades/grade_form.html', grade=grade, teachers=teachers, title='Editar Grado')
            
            grade_data = {
                'grade_name': grade_name,
                'director_teacher_id': director_teacher_id
            }
            
            success = update_grade(current_app.config['DB_CONFIG'], grade_id, grade_data)
            
            if success:
                flash("Grado actualizado exitosamente", "success")
                return redirect(url_for('grades.list_grades'))
            else:
                flash("Error al actualizar grado", "error")
                teachers = get_all_teachers(current_app.config['DB_CONFIG'])
                grade = get_grade_by_id(current_app.config['DB_CONFIG'], grade_id)
                return render_template('grades/grade_form.html', grade=grade, teachers=teachers, title='Editar Grado')
        
        except Exception as e:
            flash(f"Error al actualizar grado: {str(e)}", "error")
            teachers = get_all_teachers(current_app.config['DB_CONFIG'])
            grade = get_grade_by_id(current_app.config['DB_CONFIG'], grade_id)
            return render_template('grades/grade_form.html', grade=grade, teachers=teachers, title='Editar Grado')
    
    else:  # GET request
        try:
            grade = get_grade_by_id(current_app.config['DB_CONFIG'], grade_id)
            if grade:
                teachers = get_all_teachers(current_app.config['DB_CONFIG'])
                return render_template('grades/grade_form.html', grade=grade, teachers=teachers, title='Editar Grado')
            else:
                flash("Grado no encontrado", "error")
                return redirect(url_for('grades.list_grades'))
        except Exception as e:
            flash(f"Error al obtener datos del grado: {str(e)}", "error")
            return redirect(url_for('grades.list_grades'))

@grades_bp.route('/<int:grade_id>/delete', methods=['POST'])
def delete_grade_route(grade_id):
    """Elimina un grado si no tiene estudiantes asociados."""
    try:
        grade = get_grade_by_id(current_app.config['DB_CONFIG'], grade_id)
        
        if not grade:
            flash("Grado no encontrado", "error")
            return redirect(url_for('grades.list_grades'))
        
        success = delete_grade(current_app.config['DB_CONFIG'], grade_id)
        
        if success:
            flash("Grado eliminado exitosamente", "success")
        else:
            # Si no se puede eliminar, probablemente sea porque tiene estudiantes asociados
            students = get_grade_students(current_app.config['DB_CONFIG'], grade_id)
            if students:
                flash(f"No se puede eliminar el grado porque tiene {len(students)} estudiantes asignados", "warning")
            else:
                flash("Error al eliminar grado", "error")
                
        return redirect(url_for('grades.list_grades'))
    
    except Exception as e:
        flash(f"Error al eliminar grado: {str(e)}", "error")
        return redirect(url_for('grades.list_grades'))