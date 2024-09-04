import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter import Label, Button

def abrirImagen():
    """Abre un diálogo para seleccionar una imagen y la muestra en la interfaz."""
    rutaArchivo = filedialog.askopenfilename()
    if rutaArchivo:
        global rutaImagenOriginal
        rutaImagenOriginal = rutaArchivo  # Guardar la ruta para su uso posterior
        imagen = Image.open(rutaArchivo)
        
        # Redimensionar la imagen a 250x250
        imagenMostrada = imagen.resize((250, 250), Image.Resampling.LANCZOS)
        
        imagenMostrada = ImageTk.PhotoImage(imagenMostrada)
        etiquetaOriginal.config(image=imagenMostrada)
        etiquetaOriginal.image = imagenMostrada
        
        # Limpiar la imagen procesada
        etiquetaProcesada.config(image='')
        botonProcesar.config(state=tk.NORMAL)


def procesarImagen():
    """Convierte la imagen a blanco y negro y la muestra en la interfaz."""
    rutaArchivo = rutaImagenOriginal
    imagen = Image.open(rutaArchivo)
    imagenBlancoNegro = ImageOps.grayscale(imagen)  # Convierte la imagen a blanco y negro
    
    # Mostrar la imagen procesada
    imagenMostrada = ImageOps.fit(imagenBlancoNegro, (250, 250), method=Image.Resampling.LANCZOS)
    imagenMostrada = ImageTk.PhotoImage(imagenMostrada)
    etiquetaProcesada.config(image=imagenMostrada)
    etiquetaProcesada.image = imagenMostrada

# Crear la ventana principal
ventanaPrincipal = tk.Tk()
ventanaPrincipal.title("Editor de Imágenes")

# Crear y ubicar los widgets
marco = tk.Frame(ventanaPrincipal)
marco.pack()

etiquetaOriginal = Label(marco)
etiquetaOriginal.grid(row=0, column=0, padx=10, pady=10)

etiquetaProcesada = Label(marco)
etiquetaProcesada.grid(row=0, column=1, padx=10, pady=10)

botonAbrir = Button(ventanaPrincipal, text="Abrir Imagen", command=abrirImagen)
botonAbrir.pack(pady=10)

botonProcesar = Button(ventanaPrincipal, text="Convertir a Blanco y Negro", command=procesarImagen, state=tk.DISABLED)
botonProcesar.pack(pady=10)

# Variable global para almacenar la ruta de la imagen original
rutaImagenOriginal = None

# Iniciar el loop de la interfaz
ventanaPrincipal.mainloop()
