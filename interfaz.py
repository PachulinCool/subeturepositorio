from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sistema import Sistema
from curso import Curso
from estudiante import Estudiante
from tkinter import Scrollbar

class Interfaz():
    def __init__(self, ventana):
        self.ventana = ventana
        self.sistema = Sistema(self)
        self.curso_actual = None
        self.dibujarComponentes()

    def dibujarComponentes(self):
        self.ventana.title("Sistema de Calificaciones")
        self.ventana.geometry("800x600")

        # Crea un marco para contener todos los elementos que quieres centrar
        frame = Frame(self.ventana)
        frame.pack(pady=30)

        Label(frame, text="Nombre del curso: ").grid(row=0, column=0)
        self.nombre_curso = Entry(frame)
        self.nombre_curso.grid(row=0, column=1)

        Button(frame, text="Crear curso", command=self.crear_curso).grid(row=1, column=0)

        Label(frame, text="Seleccionar curso: ").grid(row=1, column=1)
        self.combo_cursos = ttk.Combobox(frame, state="readonly")
        self.combo_cursos.grid(row=1, column=2)
        self.combo_cursos.bind("<<ComboboxSelected>>", self.seleccionar_curso)

        Label(frame, text="Codigo del estudiante: ").grid(row=2, column=0)
        self.codigo_estudiante = Entry(frame)
        self.codigo_estudiante.grid(row=2, column=1)

        Label(frame, text="Apellidos del estudiante: ").grid(row=3, column=0)
        self.apellidos_estudiante = Entry(frame)
        self.apellidos_estudiante.grid(row=3, column=1)

        Label(frame, text="Nombre del estudiante: ").grid(row=4, column=0)
        self.nombre_estudiante = Entry(frame)
        self.nombre_estudiante.grid(row=4, column=1)

        Button(frame, text="Agregar estudiante", command=self.agregar_estudiante).grid(row=10, column=0)

        self.notas = []
        self.porcentajes = []
        for i in range(3):  # Cambia el rango a 3 para que solo se creen 3 notas
            Label(frame, text=f"Nota {i+1}: ").grid(row=6+i, column=0)
            nota = Entry(frame)
            nota.grid(row=6+i, column=1)
            self.notas.append(nota)

            Label(frame, text=f"Porcentaje {i+1}: ").grid(row=6+i, column=2)
            porcentaje = Entry(frame)
            porcentaje.grid(row=6+i, column=3)
            self.porcentajes.append(porcentaje)

        # Agrega una entrada separada para la asistencia
        Label(frame, text="Asistencia: ").grid(row=9, column=0)
        self.asistencia = Entry(frame)
        self.asistencia.grid(row=9, column=1)
        self.notas.append(self.asistencia)

        # Agrega una entrada separada para el porcentaje de la asistencia
        Label(frame, text="Porcentaje Asistencia: ").grid(row=9, column=2)
        porcentaje_asistencia = Entry(frame)
        porcentaje_asistencia.grid(row=9, column=3)
        self.porcentajes.append(porcentaje_asistencia)

        # Crea un marco para contener la tabla y la barra de desplazamiento
        frame_tabla = Frame(self.ventana)
        frame_tabla.place(x=10, y=340)

        self.tabla = ttk.Treeview(frame_tabla, columns=("Codigo", "Apellidos", "Nombre", "Nota1", "Nota2", "Nota3", "Asistencia", "Definitiva"))
        self.tabla["show"] = "headings"
        self.tabla.column("Codigo", width=100)
        self.tabla.column("Asistencia", width=110)
        self.tabla.column("Definitiva", width=110)
        self.tabla.heading("Codigo", text="Codigo")
        self.tabla.heading("Apellidos", text="Apellidos")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Nota1", text="Nota 1")
        self.tabla.heading("Nota2", text="Nota 2")
        self.tabla.heading("Nota3", text="Nota 3")
        self.tabla.heading("Asistencia", text="Asistencia")
        self.tabla.heading("Definitiva", text="Definitiva")
        self.tabla.pack(side='left', fill='both')  # Posiciona la tabla en el marco

        # Crea un nuevo marco para el combobox de selección de tablas
        frame_tablas = Frame(self.ventana)
        frame_tablas.pack(pady=30)

        Label(frame, text="Seleccionar tabla: ").grid(row=12, column=0)
        self.combo_tablas = ttk.Combobox(frame, state="readonly")
        self.combo_tablas.grid(row=12, column=1)
        self.combo_tablas.bind("<<ComboboxSelected>>", self.seleccionar_tabla)



    def crear_curso(self):
        nombre = self.nombre_curso.get()
        if not nombre:  # Verifica si el nombre está vacío
            messagebox.showerror("Error", "El nombre del curso no puede estar vacío.")
            return
        curso = Curso(nombre)
        self.sistema.agregar_curso(curso)
        self.nombre_curso.delete(0, 'end')  # Limpia la caja de texto del nombre del curso
        self.combo_cursos['values'] = list(self.sistema.cursos.keys())  # Actualiza los valores del ComboBox

    def seleccionar_curso(self, event):
        nombre = self.combo_cursos.get()
        if nombre in self.sistema.cursos:  # Verifica si el nombre existe en las claves del diccionario
            self.curso_actual = self.sistema.seleccionar_curso(nombre)
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", f"No se encontró el curso con el nombre {nombre}")    

    def agregar_estudiante(self):
        codigo = self.codigo_estudiante.get()
        apellidos = self.apellidos_estudiante.get()
        nombre = self.nombre_estudiante.get()
        estudiante = Estudiante(nombre, apellidos, codigo)
        for est in self.curso_actual.estudiantes:
            if est.codigo == estudiante.codigo:
                messagebox.showwarning("Advertencia", "El código del estudiante ya existe en este curso.")
                return
        if not codigo or not apellidos or not nombre:
            messagebox.showerror("Error", "Por favor, llena todos los campos.")
            return
        for i in range(4):
            nota_entrada = self.notas[i].get()
            porcentaje_entrada = self.porcentajes[i].get()
            if not nota_entrada or not porcentaje_entrada:
                messagebox.showerror("Error", "Por favor, llena todos los campos.")
                return
            nota = float(nota_entrada)
            porcentaje = float(porcentaje_entrada)
            if not 1 <= nota <= 5:
                messagebox.showerror("Error", "Las notas deben estar entre 1 y 5.")
                return
            nota = round(nota * porcentaje / 100, 2)
            if i == 0:
                estudiante.nota1 = nota
            elif i == 1:
                estudiante.nota2 = nota
            elif i == 2:
                estudiante.nota3 = nota
            elif i == 3:
                estudiante.nota4 = nota

        # Calcula la nota definitiva del estudiante
        estudiante.calcular_definitiva()

        self.curso_actual.estudiantes.append(estudiante)
        self.sistema.guardar_curso(self.curso_actual)
        self.actualizar_tabla()
        self.actualizar_tablas()
        # Limpia los campos de entrada
        self.codigo_estudiante.delete(0, 'end')
        self.apellidos_estudiante.delete(0, 'end')
        self.nombre_estudiante.delete(0, 'end')
        for i in range(4):
            self.notas[i].delete(0, 'end')

    def calcular_definitivas(self):
        self.curso_actual.calcular_definitivas()
        self.actualizar_tabla()
        
    def seleccionar_tabla(self, event):
        tabla_seleccionada = self.combo_tablas.get()
        cursor = self.sistema.conn.cursor()
        cursor.execute(f"SELECT * FROM {tabla_seleccionada}")
        estudiantes_db = cursor.fetchall()
        # Limpia la tabla de la GUI
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        # Llena la tabla de la GUI con la información de la tabla seleccionada
        for estudiante_db in estudiantes_db:
            self.tabla.insert('', 'end', text=estudiante_db[0], values=(estudiante_db[0], estudiante_db[1], estudiante_db[2], estudiante_db[3], estudiante_db[4], estudiante_db[5], estudiante_db[6], estudiante_db[7]))

    def actualizar_tabla(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for estudiante in self.curso_actual.estudiantes:
            estudiante.calcular_definitiva()  # Asegúrate de que la nota definitiva esté actualizada
            if None not in [estudiante.nota1, estudiante.nota2, estudiante.nota3, estudiante.nota4]:
                self.tabla.insert('', 'end', text=estudiante.codigo, values=(estudiante.codigo, estudiante.apellido, estudiante.nombre, estudiante.nota1, estudiante.nota2, estudiante.nota3, estudiante.nota4, estudiante.definitiva))
            else:
                messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")

    def actualizar_cursos(self):
        nombres_cursos = list(self.sistema.cursos.keys())
        self.combo_cursos['values'] = nombres_cursos

    def actualizar_tablas(self):
        cursor = self.sistema.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        nombres_tablas = [nombre[0] for nombre in cursor.fetchall()]
        self.combo_tablas['values'] = nombres_tablas





