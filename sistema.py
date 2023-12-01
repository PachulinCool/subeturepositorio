import sqlite3
from curso import Curso
from estudiante import Estudiante

class Sistema():
    def __init__(self, interfaz):
        self.interfaz = interfaz
        self.conn = sqlite3.connect('cursos.db')
        self.cursos = {}
        self.cargar_cursos()

    def cargar_cursos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        nombres_cursos = cursor.fetchall()
        for nombre_curso in nombres_cursos:
            cursor.execute(f"SELECT * from {nombre_curso[0]}")
            estudiantes_db = cursor.fetchall()
            curso = Curso(nombre_curso[0])
            for estudiante_db in estudiantes_db:
                estudiante = Estudiante(estudiante_db[0], estudiante_db[1], estudiante_db[2])
                estudiante.notas = estudiante_db[3]
                curso.estudiantes.append(estudiante)
            self.cursos[nombre_curso[0]] = curso

    def agregar_curso(self, curso):
        if curso.nombre:
            self.cursos[curso.nombre] = curso
            cursor = self.conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTs {curso.nombre} (codigo TEXT, apellido TEXT, nombre TEXT, nota1 REAL, nota2 REAL, nota3 REAL, nota4 REAL, definitiva REAL)")
            self.conn.commit()
        else:
            raise ValueError("El nombre del curso no puede estar vacío.")

    def guardar_curso(self, curso):
        cursor = self.conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {curso.nombre} (codigo TEXT, apellido TEXT, nombre TEXT, nota1 REAL, nota2 REAL, nota3 REAL, nota4 REAL, definitiva REAL)")
        for estudiante in curso.estudiantes:
            cursor.execute(f"INSERT INTO {curso.nombre} VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (estudiante.codigo, estudiante.apellido, estudiante.nombre, estudiante.nota1, estudiante.nota2, estudiante.nota3, estudiante.nota4, estudiante.definitiva))
            if estudiante.definitiva is not None:
                tabla = f"{curso.nombre}_aprobado" if estudiante.definitiva >= 3 else f"{curso.nombre}_reprobado"
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {tabla} (codigo TEXT, apellido TEXT, nombre TEXT, nota1 REAL, nota2 REAL, nota3 REAL, nota4 REAL, definitiva REAL)")
                cursor.execute(f"INSERT INTO {tabla} VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               (estudiante.codigo, estudiante.apellido, estudiante.nombre, estudiante.nota1, estudiante.nota2, estudiante.nota3, estudiante.nota4, estudiante.definitiva))
        self.conn.commit()

    def seleccionar_curso(self, nombre):
        if nombre in self.cursos:
            return self.cursos[nombre]
        else:
            raise KeyError(f"No se encontró el curso con el nombre {nombre}")


