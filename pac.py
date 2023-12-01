from tkinter import Tk
from interfaz import Interfaz

class ProgramaPrincipal:
    def __init__(self):
        self.ventana = Tk()
        self.interfaz = Interfaz(self.ventana)

    def ejecutar(self):
        self.ventana.mainloop()


programa = ProgramaPrincipal()
programa.ejecutar()
