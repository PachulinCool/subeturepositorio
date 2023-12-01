class Estudiante():
    def __init__(self, nombre_completo, apellido, codigo):
        self.nombre = nombre_completo
        self.apellido = apellido
        self.codigo = codigo
        self.nota1 = None
        self.nota2 = None
        self.nota3 = None
        self.nota4 = None
        self.definitiva = None

    def agregar_nota(self, nota, porcentaje, nota_numero):
        nota_ponderada = nota * porcentaje
        if nota_numero == 1:
            self.nota1 = nota_ponderada
        elif nota_numero == 2:
            self.nota2 = nota_ponderada
        elif nota_numero == 3:
            self.nota3 = nota_ponderada
        elif nota_numero == 4:
            self.nota4 = nota_ponderada
        self.calcular_definitiva()

    def calcular_definitiva(self):
        self.definitiva = round(self.nota1 + self.nota2 + self.nota3 + self.nota4, 2)

