# Institución Educativa "El Futuro del Saber" - Gestión Escolar

## Descripción

Esta es una aplicación web desarrollada con Flask para la gestión de información académica básica de la Institución Educativa "El Futuro del Saber". Permite administrar estudiantes, docentes, asignaturas y grados, así como la inscripción de estudiantes a asignaturas.

**Nota Importante:** Esta aplicación funciona como un sitio web tradicional. Las rutas (endpoints) definidas a continuación renderizan y devuelven páginas HTML completas al navegador, no respuestas en formato JSON como lo haría una API REST dedicada.

## Características

*   **Gestión de Estudiantes:** Crear, ver detalles, editar y eliminar registros de estudiantes.
*   **Gestión de Docentes:** Crear, ver detalles, editar y eliminar registros de docentes.
*   **Gestión de Asignaturas:** Crear, editar, eliminar asignaturas y asignarles un profesor.
*   **Gestión de Grados:** Crear, ver detalles, editar, eliminar grados y asignarles un director de grupo.
*   **Inscripción de Estudiantes:** Inscribir y retirar estudiantes de las asignaturas.
*   **Panel Principal:** Muestra estadísticas básicas (total de estudiantes, docentes, etc.) y el estado de la conexión a la base de datos.
*   **Interfaz Web:** Basada en Bootstrap 5 para una experiencia de usuario limpia y responsiva.
*   **Validación:** Validación básica del lado del cliente en los formularios para campos requeridos.

## Estructura del Proyecto

```
institucion_app/
├── app.py                  # Archivo principal de la aplicación Flask
├── requirements.txt        # Dependencias de Python
├── README.md               # Este archivo
├── core/                   # Directorio principal del código fuente
│   ├── __init__.py
│   ├── db/                 # Módulos de acceso a la base de datos
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── student_db.py
│   │   ├── teacher_db.py
│   │   ├── subject_db.py
│   │   └── grade_db.py
│   ├── routes/             # Definición de rutas (Blueprints)
│   │   ├── __init__.py
│   │   ├── student_routes.py
│   │   ├── teacher_routes.py
│   │   ├── subject_routes.py
│   │   └── grade_routes.py
│   └── templates/          # Plantillas HTML (Jinja2)
│       ├── base.html
│       ├── index.html
│       ├── students/
│       ├── teachers/
│       ├── subjects/
│       └── grades/
└── static/                 # Archivos estáticos (CSS, JS, .env)
    ├── css/
    │   └── styles.css
    └── .env                # Archivo de variables de entorno (¡IMPORTANTE!)
```

## Instrucciones de Configuración

1.  **Clonar el Repositorio (si aplica):**
    ```bash
    git clone https://github.com/Danidiaz0799/institucion_app.git
    cd institucion_app
    ```

2.  **Crear un Entorno Virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Base de Datos:**
    *   Asegúrate de tener un servidor MySQL en ejecución.
    *   Crea una base de datos (p.ej., `institucion_el_futuro`).
    *   Ejecuta el script SQL proporcionado en `query/queryDb.sql` en tu base de datos recién creada para generar las tablas necesarias. Puedes usar una herramienta como MySQL Workbench, DBeaver, o la línea de comandos de `mysql`:
        ```bash
        # Ejemplo usando la línea de comandos
        mysql -u tu_usuario_mysql -p institucion_el_futuro < query/queryDb.sql
        ```

5.  **Configurar Variables de Entorno:**
    *   Crea un archivo llamado `.env` dentro del directorio `static/`.
    *   Añade las siguientes variables con tus credenciales de base de datos y una clave secreta para Flask:
        ```dotenv
        DB_HOST=localhost
        DB_USER=tu_usuario_mysql
        DB_PASSWORD=tu_contraseña_mysql
        DB_NAME=institucion_el_futuro
        FLASK_SECRET_KEY=genera_una_clave_segura_aqui
        ```
    *   **Nota:** Asegúrate de que `app.py` esté cargando correctamente el archivo `.env` desde la ubicación `static/`.

6.  **Ejecutar la Aplicación:**
    ```bash
    python app.py
    ```
    La aplicación estará disponible por defecto en `http://127.0.0.1:5000/`.

## Endpoints (Rutas Web)

La aplicación utiliza Blueprints de Flask para organizar las rutas. Todas las rutas devuelven páginas HTML.

### Principal (`app.py`)

*   `GET /`: Muestra la página de inicio (`index.html`) con estadísticas.
*   `GET /update_index`: (Ruta de utilidad interna, actualiza enlaces en `index.html`).

### Estudiantes (`/students`)

*   `GET /`: Muestra la lista de todos los estudiantes.
*   `GET /new`: Muestra el formulario para crear un nuevo estudiante.
*   `POST /new`: Procesa la creación de un nuevo estudiante.
*   `GET /<int:student_id>`: Muestra los detalles de un estudiante específico.
*   `GET /<int:student_id>/edit`: Muestra el formulario para editar un estudiante.
*   `POST /<int:student_id>/edit`: Procesa la actualización de un estudiante.
*   `POST /<int:student_id>/delete`: Elimina un estudiante.

### Docentes (`/teachers`)

*   `GET /`: Muestra la lista de todos los docentes.
*   `GET /new`: Muestra el formulario para crear un nuevo docente.
*   `POST /new`: Procesa la creación de un nuevo docente.
*   `GET /<int:teacher_id>`: Muestra los detalles de un docente específico.
*   `GET /<int:teacher_id>/edit`: Muestra el formulario para editar un docente.
*   `POST /<int:teacher_id>/edit`: Procesa la actualización de un docente.
*   `POST /<int:teacher_id>/delete`: Elimina un docente.

### Asignaturas (`/subjects`)

*   `GET /`: Muestra la lista de todas las asignaturas.
*   `GET /new`: Muestra el formulario para crear una nueva asignatura.
*   `POST /new`: Procesa la creación de una nueva asignatura.
*   `GET /<int:subject_id>/edit`: Muestra el formulario para editar una asignatura.
*   `POST /<int:subject_id>/edit`: Procesa la actualización de una asignatura.
*   `POST /<int:subject_id>/delete`: Elimina una asignatura.
*   `GET /<int:subject_id>/manage_students`: Muestra la página para inscribir/retirar estudiantes de una asignatura.
*   `POST /<int:subject_id>/manage_students`: Procesa la inscripción o retiro de estudiantes de la asignatura.

### Grados (`/grades`)

*   `GET /`: Muestra la lista de todos los grados.
*   `GET /new`: Muestra el formulario para crear un nuevo grado.
*   `POST /new`: Procesa la creación de un nuevo grado.
*   `GET /<int:grade_id>`: Muestra los detalles de un grado específico.
*   `GET /<int:grade_id>/edit`: Muestra el formulario para editar un grado.
*   `POST /<int:grade_id>/edit`: Procesa la actualización de un grado.
*   `POST /<int:grade_id>/delete`: Elimina un grado (si no tiene estudiantes).

## Esquema de la Base de Datos

Basado en el diagrama proporcionado:

*   **`teachers`**
    *   `teacher_id` (PK, INT, Auto Increment)
    *   `id_type` (VARCHAR)
    *   `id_number` (VARCHAR, Unique)
    *   `first_name` (VARCHAR)
    *   `last_name` (VARCHAR)
    *   `birth_date` (DATE)
    *   `education_level` (VARCHAR)
    *   `email` (VARCHAR, Unique)
    *   `phone_landline` (VARCHAR)
    *   `phone_mobile` (VARCHAR)
*   **`grades`**
    *   `grade_id` (PK, INT, Auto Increment)
    *   `grade_name` (VARCHAR, Unique)
    *   `director_teacher_id` (FK -> teachers.teacher_id, INT, Nullable)
*   **`students`**
    *   `student_id` (PK, INT, Auto Increment)
    *   `grade_id` (FK -> grades.grade_id, INT)
    *   `id_type` (VARCHAR)
    *   `id_number` (VARCHAR, Unique)
    *   `first_name` (VARCHAR)
    *   `last_name` (VARCHAR)
    *   `birth_date` (DATE)
    *   `residence_city` (VARCHAR)
    *   `address` (VARCHAR)
    *   `email` (VARCHAR, Unique)
    *   `phone_landline` (VARCHAR)
    *   `phone_mobile` (VARCHAR)
    *   `guardian_full_name` (VARCHAR)
*   **`subjects`**
    *   `subject_id` (PK, INT, Auto Increment)
    *   `teacher_id` (FK -> teachers.teacher_id, INT, Nullable)
    *   `subject_name` (VARCHAR, Unique)
*   **`student_subjects`** (Tabla Intermedia)
    *   `student_id` (PK, FK -> students.student_id, INT)
    *   `subject_id` (PK, FK -> subjects.subject_id, INT)

*(PK = Clave Primaria, FK = Clave Foránea)* 