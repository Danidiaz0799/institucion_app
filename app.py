# app.py
import os
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env, especificando la ruta
# Guardamos el resultado para ver si encontró el archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), 'static', '.env')
print(f"Intentando cargar .env desde: {dotenv_path}") # Línea de depuración adicional
dotenv_loaded = load_dotenv(dotenv_path=dotenv_path)

# --- INICIO: Bloque de Depuración ---
print("--- Debugging Environment Variables ---")
print(f"Archivo .env cargado: {dotenv_loaded}") # Debería ser True si encontró el archivo
print(f"DB_HOST leído: {os.getenv('DB_HOST')}")
print(f"DB_USER leído: {os.getenv('DB_USER')}") # ¡Este es el valor clave a verificar!
print(f"DB_PASSWORD leído: {'******' if os.getenv('DB_PASSWORD') else None}") # No imprimimos la contraseña real
print(f"DB_NAME leído: {os.getenv('DB_NAME')}")
print("------------------------------------")
# --- FIN: Bloque de Depuración ---

# Inicializar la aplicación Flask con la carpeta de templates personalizada
app = Flask(__name__, template_folder='core/templates')

# Configurar una clave secreta para la sesión de Flask
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key_change_me')

# Configuración de la conexión a la base de datos
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'institucion_el_futuro')
}

# Configuramos una clave en la aplicación para pasar la configuración de la BD a los blueprints
app.config['DB_CONFIG'] = db_config

# Función para obtener una conexión a la base de datos (sin cambios)
def get_db_connection():
    """Crea y retorna una conexión a la base de datos y un cursor."""
    try:
        # Usamos la variable global db_config que se definió arriba con los valores leídos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        return conn, cursor
    except Error as e:
        # Imprimimos el usuario que intentó usar para más claridad en el error
        print(f"Error al conectar a MySQL como usuario '{db_config.get('user')}': {e}")
        return None, None

# Ruta principal (Index) - Modificada para probar la conexión a la BD (sin cambios recientes)
@app.route('/')
def index():
    """Página principal con estadísticas y estado del sistema."""
    conn = None
    cursor = None
    db_status = "Desconectado"
    db_name = "N/A"
    student_count = 0
    teacher_count = 0
    subject_count = 0
    grade_count = 0
    current_date = ""

    try:
        from datetime import datetime
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        conn, cursor = get_db_connection()
        if conn and conn.is_connected() and cursor:
            # Obtener el nombre de la base de datos
            cursor.execute("SELECT DATABASE();")
            result = cursor.fetchone()
            if result:
                db_name = result['DATABASE()']
                db_status = "Conectado"
            else:
                db_status = "Conectado, pero no se pudo obtener el nombre de la BD."
            
            # Obtener conteo de estudiantes
            cursor.execute("SELECT COUNT(*) as count FROM students")
            result = cursor.fetchone()
            student_count = result['count'] if result else 0
            
            # Obtener conteo de profesores
            cursor.execute("SELECT COUNT(*) as count FROM teachers")
            result = cursor.fetchone()
            teacher_count = result['count'] if result else 0
            
            # Obtener conteo de asignaturas
            cursor.execute("SELECT COUNT(*) as count FROM subjects")
            result = cursor.fetchone()
            subject_count = result['count'] if result else 0
            
            # Obtener conteo de grados
            cursor.execute("SELECT COUNT(*) as count FROM grades")
            result = cursor.fetchone()
            grade_count = result['count'] if result else 0
        else:
            db_status = "Error al obtener conexión/cursor."

    except Error as e:
        db_status = f"Error de consulta: {e}"
    except Exception as e:
        print(f"Error no esperado: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return render_template('index.html', 
                          title='Inicio', 
                          db_status=db_status, 
                          db_name=db_name,
                          current_date=current_date,
                          student_count=student_count,
                          teacher_count=teacher_count,
                          subject_count=subject_count,
                          grade_count=grade_count)

# Importar e registrar los blueprints
from core.routes.student_routes import students_bp
from core.routes.teacher_routes import teachers_bp
from core.routes.subject_routes import subjects_bp
from core.routes.grade_routes import grades_bp

app.register_blueprint(students_bp, url_prefix='/students')
app.register_blueprint(teachers_bp, url_prefix='/teachers')
app.register_blueprint(subjects_bp, url_prefix='/subjects')
app.register_blueprint(grades_bp, url_prefix='/grades')

# Actualizar el enlace en index.html
@app.route('/update_index')
def update_index():
    try:
        with open('core/templates/index.html', 'r') as file:
            content = file.read()
        
        # Actualizar el enlace a estudiantes
        updated_content = content.replace('<li><a href="#">Gestionar Estudiantes</a></li>', 
                                         '<li><a href="{{ url_for(\'students.list_students\') }}">Gestionar Estudiantes</a></li>')
        
        # Actualizar el enlace a profesores
        updated_content = updated_content.replace('<a href="#" class="btn btn-secondary">Próximamente</a>', 
                                              '<a href="{{ url_for(\'teachers.list_teachers\') }}" class="btn btn-primary">Acceder</a>')
        
        with open('core/templates/index.html', 'w') as file:
            file.write(updated_content)
        
        flash("Plantilla de inicio actualizada correctamente.", "success")
    except Exception as e:
        flash(f"Error al actualizar la plantilla de inicio: {e}", "error")
    
    return redirect(url_for('index'))

# --- Bloque para ejecutar la aplicación (sin cambios) ---
if __name__ == '__main__':
    app.run(debug=True)