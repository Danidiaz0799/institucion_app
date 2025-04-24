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
    """Página principal, ahora también prueba la conexión a la BD."""
    conn = None
    cursor = None
    db_status = "Desconectado"
    db_name = "N/A"

    try:
        conn, cursor = get_db_connection()
        if conn and conn.is_connected() and cursor:
            cursor.execute("SELECT DATABASE();")
            result = cursor.fetchone()
            if result:
                db_name = result['DATABASE()']
                db_status = "Conectado"
                # print(f"Conexión exitosa a la base de datos: {db_name}") # Ya no es necesario aquí
            else:
                 db_status = "Conectado, pero no se pudo obtener el nombre de la BD."
        else:
             # Este es el mensaje que probablemente ves en la web ahora
             db_status = "Error al obtener conexión/cursor."

    except Error as e:
        db_status = f"Error de consulta: {e}"
        # print(f"Error durante la consulta de prueba: {e}") # Ya no es necesario aquí

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return render_template('index.html', title='Inicio', db_status=db_status, db_name=db_name)

# Importar e registrar los blueprints
from core.routes.student_routes import students_bp
from core.routes.teacher_routes import teachers_bp

app.register_blueprint(students_bp, url_prefix='/students')
app.register_blueprint(teachers_bp, url_prefix='/teachers')

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