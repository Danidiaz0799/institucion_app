-- Script SQL para Crear la Base de Datos y Tablas para 'Institucion Educativa El Futuro del Saber'
-- Basado en el Modelo E-R definido previamente.

-- -----------------------------------------------------
-- Creación de la Base de Datos
-- -----------------------------------------------------
-- Crea la base de datos si no existe, usando el conjunto de caracteres y collation por defecto del servidor.
CREATE DATABASE IF NOT EXISTS institucion_el_futuro;

-- Selecciona la base de datos a usar para los comandos siguientes.
USE institucion_el_futuro;

-- -----------------------------------------------------
-- Tabla `teachers`
-- Almacena información sobre los docentes.
-- Contiene detalles personales, de contacto y profesionales.
-- Es referenciada por `grades` (para el director) y `subjects` (para el instructor).
-- -----------------------------------------------------
CREATE TABLE teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    id_type VARCHAR(10) NOT NULL,
    id_number VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE,
    education_level VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone_landline VARCHAR(20),
    phone_mobile VARCHAR(20)
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Tabla `grades`
-- Almacena información sobre los grados/niveles en la institución (ej. Primero, Segundo A).
-- Cada grado tiene un nombre y opcionalmente puede tener un director asignado de la tabla `teachers`.
-- Es referenciada por la tabla `students`.
-- -----------------------------------------------------
CREATE TABLE grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    grade_name VARCHAR(100) NOT NULL UNIQUE,
    director_teacher_id INT UNIQUE,
    FOREIGN KEY (director_teacher_id) REFERENCES teachers(teacher_id)
        ON DELETE SET NULL -- Si se borra el docente director, el grado queda sin director.
        ON UPDATE CASCADE -- Si el ID del docente director cambia, se actualiza aquí también.
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Tabla `students`
-- Almacena información sobre los estudiantes.
-- Contiene detalles personales, de contacto, del acudiente y el grado en el que está matriculado.
-- Referencia a la tabla `grades`. Es referenciada por la tabla `student_subjects`.
-- -----------------------------------------------------
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    grade_id INT NOT NULL,
    id_type VARCHAR(10) NOT NULL,
    id_number VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE,
    residence_city VARCHAR(100),
    address VARCHAR(255),
    email VARCHAR(100) UNIQUE,
    phone_landline VARCHAR(20),
    phone_mobile VARCHAR(20),
    guardian_full_name VARCHAR(200),
    FOREIGN KEY (grade_id) REFERENCES grades(grade_id)
        ON DELETE RESTRICT -- Previene borrar un grado si todavía tiene estudiantes matriculados.
        ON UPDATE CASCADE -- Si el ID del grado referenciado cambia, se actualiza aquí también.
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Tabla `subjects`
-- Almacena información sobre las asignaturas ofrecidas.
-- Cada asignatura tiene un nombre y es dictada por un docente de la tabla `teachers`.
-- Es referenciada por la tabla `student_subjects`.
-- -----------------------------------------------------
CREATE TABLE subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL,
    subject_name VARCHAR(100) NOT NULL UNIQUE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
        ON DELETE RESTRICT -- Previene borrar un docente si está asignado a dictar asignaturas.
        ON UPDATE CASCADE -- Si el ID del docente referenciado cambia, se actualiza aquí también.
) ENGINE=InnoDB;

-- -----------------------------------------------------
-- Tabla `student_subjects`
-- Tabla de mapeo para la relación Muchos-a-Muchos entre estudiantes y asignaturas.
-- Almacena qué estudiante está matriculado en qué asignatura.
-- Referencia a las tablas `students` y `subjects`.
-- -----------------------------------------------------
CREATE TABLE student_subjects (
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    PRIMARY KEY (student_id, subject_id), -- Llave primaria compuesta
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE -- Si se borra un estudiante, sus registros de matrícula aquí también se borran.
        ON UPDATE CASCADE, -- Si el ID de un estudiante cambia, se actualiza aquí también.
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        ON DELETE CASCADE -- Si se borra una asignatura, sus registros de matrícula aquí también se borran.
        ON UPDATE CASCADE -- Si el ID de una asignatura cambia, se actualiza aquí también.
) ENGINE=InnoDB;


