from tkinter import *
from tkinter import messagebox
import subprocess
import os

class Subrepo():
    def __init__(self, inter):
        self.interfaz = inter
        self.interfaz.geometry("300x300")
        self.interfaz.title("sube tu repositorio")
        self.num1 = StringVar()
        self.num2 = StringVar()
        self.num3 = StringVar()
        self.num4 = StringVar()

        self.dibujarVentana()

    def dibujarVentana(self):
        Label(self.interfaz, text="Escribe la direccion de la carpeta en tu ordenador ").place(x=10, y=10)
        Entry(self.interfaz, textvariable=self.num1).place(x=20, y=30)

        Label(self.interfaz, text="Escribe el mensaje a enviar ").place(x=10, y=70)
        Entry(self.interfaz, textvariable=self.num2).place(x=20, y=90)

        Label(self.interfaz, text="Escribe nombre de usuario").place(x=10, y=120)
        Entry(self.interfaz, textvariable=self.num3).place(x=20, y=150)

        Label(self.interfaz, text="Escribe nombre de su repositorio").place(x=10, y=190)
        Entry(self.interfaz, textvariable=self.num4).place(x=20, y=220)

        Button(self.interfaz, command=self.octener, text="Subir ya").place(x=170, y=250)
        Button(self.interfaz, command=self.info, text="clik requerimientos").place(x=170, y=100)

    def octener(self):
        self.resp1 = self.num1.get()
        self.resp2 = self.num2.get()
        self.resp3 = self.num3.get()
        self.resp4 = self.num4.get()
        messagebox.showinfo("Resultado", "el repositorio se a subido con exito a la plataforma de github")
        self.lolg()

    def info(self):
        messagebox.showinfo("Resultado", "recuerde que este programa solo funcionara si usted creo una cuenta en "
                                         "github previamente y crea el espacio para su repositorio")

    def lolg(self):

        # Navegar al directorio de la carpeta
        os.chdir(self.resp1)

        # Inicializar un repositorio de Git si no existe
        subprocess.run(["git", "init"])

        # Agregar todos los archivos al área de preparación
        subprocess.run(["git", "add", "."])

        # Realizar un commit con un mensaje
        subprocess.run(["git", "commit", "-m", self.resp2])

        # Obtener la URL del repositorio de GitHub
        # Reemplaza 'nombre_usuario' y 'nombre_repositorio' con tu información real
        url_github = str("https://github.com/" + self.resp3 + "/" + self.resp4 + ".git")

        # Agregar el remoto de GitHub
        subprocess.run(["git", "remote", "add", "origin", url_github])

        # Empujar los cambios al repositorio de GitHub
        subprocess.run(["git", "push", "-u", "origin", "master"])

        print("Carpeta subida exitosamente a GitHub.")


a = Subrepo(Tk())
a.interfaz.mainloop()
