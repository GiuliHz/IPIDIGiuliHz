import tkinter as tk
from tkinter import filedialog, Label, Button, OptionMenu, StringVar
from PIL import Image, ImageTk
import numpy as np

# Función para generar Barlett
def bartlett(s=3):
    a = (s+1)//2-np.abs(np.arange(s)-s//2)
    k = np.outer(a,a.T)
    return k / k.sum()

# Función Pascal
def pascal(s=3):
    def pascal_triangle(steps, last_layer=np.array([1])):
        if steps == 1:
            return last_layer
        next_layer = np.array([1, *(last_layer[:-1] + last_layer[1:]), 1])
        return pascal_triangle(steps-1, next_layer)
    a = pascal_triangle(s)
    k = np.outer(a, a.T)
    return k / k.sum()

# Función para crear un kernel laplaciano
def laplace(_type=4, normalize=False):
    if _type == 4:
        kernel = np.array([[0., -1., 0.], [-1., 4., -1.], [0., -1., 0.]])
    if _type == 8:
        kernel = np.array([[-1., -1., -1.], [-1., 8., -1.], [-1., -1., -1.]])
    if normalize:
        kernel /= np.sum(np.abs(kernel))
    return kernel

# Función para crear un kernel Gaussiano
def gauss(size, sigma):
    ax = np.linspace(-(size // 2), size // 2, size)
    xx, yy = np.meshgrid(ax, ax)
    g = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    return g / g.sum()

# Función para crear el kernel DoG (Diferencia de Gauss)
def dog(size, fs=1, cs=2):
    return gauss(size, fs) - gauss(size, cs)

def sobel(direccion):
# Filtros básicos
    Gx = np.array([[1, 0, -1],
                   [2, 0, -2],
                   [1, 0, -1]])

    Gy = np.array([[1, 2, 1],
                   [0, 0, 0],
                   [-1, -2, -1]])

    # Generar el filtro según la dirección
    if direccion == 'Horizontal':
        return Gx
    elif direccion == 'Vertical':
        return Gy
    else:
        # Calcular el ángulo en radianes para la rotación
        angulos = {
            'Diagonal Positiva': 45,
            'Diagonal Negativa': 135,
            'Anti-Horizontal': 180,
            'Anti-Vertical': 270,
            'Anti-Diagonal Positiva': 225,
            'Anti-Diagonal Negativa': 315
        }
        
        if direccion in angulos:
            return np.rot90(Gx, angulos[direccion] // 90) if 'Anti' not in direccion else np.rot90(Gy, angulos[direccion] // 90)

# Función para expandir bordes repitiendo filas/columnas
def expandirBordes(img, kernel):
    bordeX = kernel.shape[0] // 2
    bordeY = kernel.shape[1] // 2
    imgExpandida = np.pad(img, ((bordeX, bordeX), (bordeY, bordeY)), mode='edge')
    return imgExpandida

# Función de convolución modificada con coerción
def convolucion(img, kernel):
    img = expandirBordes(img, kernel)
    resultado = np.zeros_like(img)
    
    # Aplicamos la convolución
    for x in range(img.shape[0] - kernel.shape[0] + 1):
        for y in range(img.shape[1] - kernel.shape[1] + 1):
            valor = np.sum(img[x:x+kernel.shape[0], y:y+kernel.shape[1]] * kernel)
            # Coerción: forzamos que el valor esté en el rango [0, 255] (o [0, 1] si es el caso)
            resultado[x, y] = np.clip(valor, 0, 255)  # Escala para imágenes de 8 bits en este caso

    return resultado
# Función para cargar la imagen en nivel de gris
def cargarImagen():
    rutaImagen = filedialog.askopenfilename()
    if rutaImagen:
        imagen = Image.open(rutaImagen).convert('L')  # Convertir a escala de grises
        imagenTk = ImageTk.PhotoImage(imagen)
        labelImagen.config(image=imagenTk)
        labelImagen.image = imagenTk
        global imagenOriginal
        imagenOriginal = np.array(imagen)

# Función para aplicar el filtro de convolución
def aplicarFiltroConvolucion():
    filtroSeleccionado = filtroVar.get()
    kernel = generarKernel(filtroSeleccionado)
    imagenFiltrada = convolucion(imagenOriginal, kernel)
    mostrarImagen(imagenFiltrada)

# Función para mostrar la imagen filtrada
def mostrarImagen(imagenArray):
    imagenFiltrada = Image.fromarray(np.uint8(imagenArray))
    imagenTk = ImageTk.PhotoImage(imagenFiltrada)
    labelImagen.config(image=imagenTk)
    labelImagen.image = imagenTk

# Generar el kernel según el filtro seleccionado
def generarKernel(filtro):
    if filtro == 'Pasabajos Plano 3x3':
        return np.ones((3, 3)) / 9
    elif filtro == 'Pasabajos Plano 5x5':
        return np.ones((5, 5)) / 25
    elif filtro == 'Pasabajos Plano 7x7':
        return np.ones((7, 7)) / 49
    elif filtro == 'Bartlett 3x3':
        return bartlett(3)
    elif filtro == 'Bartlett 5x5':
        return bartlett(5)
    elif filtro == 'Bartlett 7x7':
        return bartlett(7)
    elif filtro == 'Gaussiano 5x5':
        return gauss(5, 1)
    elif filtro == 'Gaussiano 7x7':
        return gauss(7, 1)
    elif filtro == 'Laplaciano v4':
        return laplace(4)
    elif filtro == 'Laplaciano v8':
        return laplace(8)
    elif filtro == 'Sobel Horizontal':
        return sobel("Horizontal")
    elif filtro == 'Sobel Vertical':
        return sobel("Vertical")
    elif filtro == 'Sobel Diagonal Positiva':
        return sobel("Diagonal Positiva")
    elif filtro == 'Sobel Diagonal Negativa':
        return sobel("Diagonal Negativa")
    elif filtro == 'Sobel Anti-Horizontal':
        return sobel("Anti-Horizontal")
    elif filtro == 'Sobel Anti-Vertical':
        return sobel("Anti-Vertical")
    elif filtro == 'Sobel Anti-Diagonal Positiva':
        return sobel("Anti-Diagonal Positiva")
    elif filtro == 'Sobel Anti-Diagonal Negativa':
        return sobel("Anti-Diagonal Negativa")

    elif filtro == 'Pasaaltos 0.2':
        laplaciano = laplace(8)
        return laplaciano * 0.2
    elif filtro == 'Pasaaltos 0.4':
        laplaciano = laplace(8)
        return laplaciano * 0.4
    return np.ones((3, 3)) / 9  # Por defecto, un filtro plano 3x3

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Aplicativo de Filtrado de Imágenes")
ventana.geometry("600x600")

# Label para mostrar la imagen
labelImagen = Label(ventana)
labelImagen.pack()

# Variable para el menú desplegable de filtros
filtroVar = StringVar(ventana)
filtroVar.set("Pasabajos Plano 3x3")  # Filtro por defecto

# Menú desplegable para seleccionar el filtro
opcionesFiltros = [
    "Pasabajos Plano 3x3", "Pasabajos Plano 5x5", "Pasabajos Plano 7x7", "Bartlett 3x3", "Bartlett 5x5", "Bartlett 7x7",
    "Gaussiano 5x5",  "Gaussiano 7x7", "Laplaciano v4", "Laplaciano v8",    "Sobel Horizontal", 
    "Sobel Vertical", 
    "Sobel Diagonal Positiva", 
    "Sobel Diagonal Negativa", 
    "Sobel Anti-Horizontal", 
    "Sobel Anti-Vertical", 
    "Sobel Anti-Diagonal Positiva", 
    "Sobel Anti-Diagonal Negativa"
    "Pasaaltos 0.2", "Pasaaltos 0.4"
]
menuFiltros = OptionMenu(ventana, filtroVar, *opcionesFiltros)
menuFiltros.pack()

# Botón para cargar la imagen
botonCargar = Button(ventana, text="Cargar Imagen", command=cargarImagen)
botonCargar.pack()

# Botón para aplicar el filtro
botonAplicar = Button(ventana, text="Aplicar Filtro", command=aplicarFiltroConvolucion)
botonAplicar.pack()

ventana.mainloop()
