class Curso():
    def __init__(self, nombre):
        self.nombre = nombre
        self.estudiantes = []

    def agregar_estudiante(self, estudiante):
        self.estudiantes.append(estudiante)

    def calcular_definitiva(self):
        notas = [self.nota1, self.nota2, self.nota3, self.nota4]
        self.definitiva = round(sum(nota for nota in notas if nota is not None), 2)


    


    
