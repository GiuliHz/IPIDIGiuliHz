import tkinter as tk
from tkinter import filedialog, Label, Button, OptionMenu, StringVar
from PIL import Image, ImageTk
import numpy as np

# Funciones de conversión entre RGB y YIQ
def rgbAYiq(imagen):
    matConversion = np.array([[0.299, 0.587, 0.114],
                              [0.595716, -0.274453, -0.321263],
                              [0.211456, -0.522591, 0.311135]])
    return np.dot(imagen / 255.0, matConversion.T)  # Normalizamos a [0,1]

def yiqARgb(imagen):
    matConversion = np.array([[1.0, 0.9563, 0.6210],
                              [1.0, -0.2721, -0.6474],
                              [1.0, -1.1070, 1.7046]])
    rgb = np.dot(imagen, matConversion.T)
    return np.clip(rgb * 255, 0, 255)

# Cuasi suma clampeada en RGB
def cuasiSumaClampeadaRgb(imagen1, imagen2):
    return np.clip(imagen1 + imagen2, 0, 255)

# Cuasi suma promediada en RGB
def cuasiSumaPromediadaRgb(imagen1, imagen2):
    return np.clip((imagen1 + imagen2) / 2, 0, 255)

# Cuasi resta clampeada en RGB
def cuasiRestaClampeadaRgb(imagen1, imagen2):
    return np.clip(imagen1 - imagen2, 0, 255).astype(np.uint8)

# Cuasi resta promediada en RGB
def cuasiRestaPromediadaRgb(imagen1, imagen2):
    return ((imagen1 - imagen2) / 2).astype(np.uint8)

# Cuasi suma clampeada en YIQ
def cuasiSumaClampeadaYiq(imagen1, imagen2):
    yiq1 = rgbAYiq(imagen1)
    yiq2 = rgbAYiq(imagen2)
    Y = np.clip(yiq1[:, :, 0] + yiq2[:, :, 0], 0, 1)
    I = (yiq1[:, :, 0] * yiq1[:, :, 1] + yiq2[:, :, 0] * yiq2[:, :, 1]) / (yiq1[:, :, 0] + yiq2[:, :, 0] + 1e-5)
    Q = (yiq1[:, :, 0] * yiq1[:, :, 2] + yiq2[:, :, 0] * yiq2[:, :, 2]) / (yiq1[:, :, 0] + yiq2[:, :, 0] + 1e-5)
    imagenResultado = np.dstack((Y, I, Q))
    return np.clip(yiqARgb(imagenResultado), 0, 255)

# Cuasi suma promediada en YIQ
def cuasiSumaPromediadaYiq(imagen1, imagen2):
    yiq1 = rgbAYiq(imagen1)
    yiq2 = rgbAYiq(imagen2)
    Y = (yiq1[:, :, 0] + yiq2[:, :, 0]) / 2
    I = (yiq1[:, :, 0] * yiq1[:, :, 1] + yiq2[:, :, 0] * yiq2[:, :, 1]) / (yiq1[:, :, 0] + yiq2[:, :, 0] + 1e-5)
    Q = (yiq1[:, :, 0] * yiq1[:, :, 2] + yiq2[:, :, 0] * yiq2[:, :, 2]) / (yiq1[:, :, 0] + yiq2[:, :, 0] + 1e-5)
    imagenResultado = np.dstack((Y, I, Q))
    return np.clip(yiqARgb(imagenResultado), 0, 255).astype(np.uint8)

# Cuasi resta clampeada en YIQ
def cuasiRestaClampeadaYiq(imagen1, imagen2):
    yiq1 = rgbAYiq(imagen1)
    yiq2 = rgbAYiq(imagen2)
    Y = np.clip(yiq1[:, :, 0] - yiq2[:, :, 0], 0, 1)
    I = (yiq1[:, :, 0] * yiq1[:, :, 1] - yiq2[:, :, 0] * yiq2[:, :, 1]) / (yiq1[:, :, 0] + yiq2[:, :, 0] + 1e-5)
    Q = (yiq1[:, :, 0] * yiq1[:, :, 2] - yiq2[:, :, 0] * yiq2[:, :, 2]) / (yiq1[:, :, 0] + yiq2[:, :, 0] + 1e-5)
    imagenResultado = np.dstack((Y, I, Q))
    return np.clip(yiqARgb(imagenResultado), 0, 255).astype(np.uint8)

# Cuasi resta promediada en YIQ
def cuasiRestaPromediadaYiq(imagen1, imagen2):
    yiq1 = rgbAYiq(imagen1)
    yiq2 = rgbAYiq(imagen2)
    Y = (yiq1[:, :, 0] - yiq2[:, :, 0]) / 2
    I = (yiq1[:, :, 0] * yiq1[:, :, 1] - yiq2[:, :, 0] * yiq2[:, :, 1]) / (yiq1[:, :, 0] + yiq2[:, :, 0] + 1e-5)
    Q = (yiq1[:, :, 0] * yiq1[:, :, 2] - yiq2[:, :, 0] * yiq2[:, :, 2]) / (yiq1[:, :, 0] + yiq2[:, :, 0] + 1e-5)
    imagenResultado = np.dstack((Y, I, Q))
    return np.clip(yiqARgb(imagenResultado), 0, 255).astype(np.uint8)

# Producto de imágenes (corregido)
def productoImagenes(imagen1, imagen2):
    # Multiplicar píxeles sin normalizar, luego normalizar en el rango [0, 255]
    producto = imagen1.astype(float) * imagen2.astype(float) / 255.0
    return np.clip(producto, 0, 255).astype(np.uint8)


# Cociente de imágenes (mejorado)
def cocienteImagenes(imagen1, imagen2):
    # Evitar divisiones por 0, y normalizamos el resultado para mantener el rango de píxeles adecuado
    cociente = imagen1 / (imagen2 + 1e-5)
    cocienteNormalizado = cociente * 255 / np.max(cociente)
    return np.clip(cocienteNormalizado, 0, 255).astype(np.uint8)


# Resta con valor absoluto
def restaValorAbsoluto(imagen1, imagen2):
    return np.clip(np.abs(imagen1 - imagen2), 0, 255).astype(np.uint8)


# If-darker: Mantiene el píxel más oscuro
def ifDarker(imagen1, imagen2):
    return np.minimum(imagen1, imagen2)

# If-lighter: Mantiene el píxel más claro
def ifLighter(imagen1, imagen2):
    return np.maximum(imagen1, imagen2)

# Función para abrir imágenes
def cargarImagen(label, imagenNum):
    global imagen1, imagen2, imagen1Tk, imagen2Tk
    ruta = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if ruta:
        img = Image.open(ruta).convert('RGB')
        label.config(text=ruta)
        img.thumbnail((300, 300))  # Redimensionar para mostrar en la interfaz
        if imagenNum == 1:
            imagen1 = np.array(img)
            imagen1Tk = ImageTk.PhotoImage(img)
            labelImagen1.config(image=imagen1Tk)
        elif imagenNum == 2:
            imagen2 = np.array(img)
            imagen2Tk = ImageTk.PhotoImage(img)
            labelImagen2.config(image=imagen2Tk)

# Función para procesar la imagen
def procesarImagen():
    global imagen1, imagen2, imagenProcesadaTk
    if imagen1 is None or imagen2 is None:
        resultadoLabel.config(text="Por favor, carga ambas imágenes")
        return

    if operacion.get() == "Cuasi Suma Clampeada RGB":
        resultadoArray = cuasiSumaClampeadaRgb(imagen1, imagen2)
    elif operacion.get() == "Cuasi Suma Promediada RGB":
        resultadoArray = cuasiSumaPromediadaRgb(imagen1, imagen2)
    elif operacion.get() == "Cuasi Resta Clampeada RGB":
        resultadoArray = cuasiRestaClampeadaRgb(imagen1, imagen2)
    elif operacion.get() == "Cuasi Resta Promediada RGB":
        resultadoArray = cuasiRestaPromediadaRgb(imagen1, imagen2)
    elif operacion.get() ==        "Cuasi Suma Clampeada YIQ":
        resultadoArray = cuasiSumaClampeadaYiq(imagen1, imagen2)
    elif operacion.get() == "Cuasi Suma Promediada YIQ":
        resultadoArray = cuasiSumaPromediadaYiq(imagen1, imagen2)
    elif operacion.get() == "Cuasi Resta Clampeada YIQ":
        resultadoArray = cuasiRestaClampeadaYiq(imagen1, imagen2)
    elif operacion.get() == "Cuasi Resta Promediada YIQ":
        resultadoArray = cuasiRestaPromediadaYiq(imagen1, imagen2)
    elif operacion.get() == "Producto de Imágenes":
        resultadoArray = productoImagenes(imagen1, imagen2)
    elif operacion.get() == "Cociente de Imágenes":
        resultadoArray = cocienteImagenes(imagen1, imagen2)
    elif operacion.get() == "Resta Valor Absoluto":
        resultadoArray = restaValorAbsoluto(imagen1, imagen2)
    elif operacion.get() == "If Darker":
        resultadoArray = ifDarker(imagen1, imagen2)
    elif operacion.get() == "If Lighter":
        resultadoArray = ifLighter(imagen1, imagen2)

    # Convertir resultado en imagen para mostrar
    resultadoImg = Image.fromarray(resultadoArray.astype('uint8'))
    resultadoImg.thumbnail((300, 300))  # Redimensionar para la interfaz
    imagenProcesadaTk = ImageTk.PhotoImage(resultadoImg)

    # Mostrar la imagen procesada
    labelImagenProcesada.config(image=imagenProcesadaTk)
    resultadoLabel.config(text="Imagen procesada mostrada.")

# Variables globales para las imágenes
imagen1 = None
imagen2 = None
imagen1Tk = None
imagen2Tk = None
imagenProcesadaTk = None

# Configuración de la interfaz
ventana = tk.Tk()
ventana.title("Aritmética de Píxeles")

# Etiquetas y botones para cargar imágenes
imagen1Label = Label(ventana)
imagen1Label.grid(row=0, column=0)

cargarImagen1Btn = Button(ventana, text="Cargar Imagen 1", command=lambda: cargarImagen(imagen1Label, 1))
cargarImagen1Btn.grid(row=1, column=0)

imagen2Label = Label(ventana)
imagen2Label.grid(row=0, column=1)

cargarImagen2Btn = Button(ventana, text="Cargar Imagen 2", command=lambda: cargarImagen(imagen2Label, 2))
cargarImagen2Btn.grid(row=1, column=1)

# Labels para mostrar las imágenes cargadas y procesadas
labelImagen1 = Label(ventana)
labelImagen1.grid(row=2, column=0)

labelImagen2 = Label(ventana)
labelImagen2.grid(row=2, column=1)

labelImagenProcesada = Label(ventana)
labelImagenProcesada.grid(row=2, column=2)

# Menú para seleccionar la operación
operacion = StringVar(ventana)
operacion.set("Cuasi Suma Clampeada RGB")  # Valor por defecto

operacionesMenu = OptionMenu(ventana, operacion, 
                             "Cuasi Suma Clampeada RGB", "Cuasi Suma Promediada RGB",
                             "Cuasi Resta Clampeada RGB", "Cuasi Resta Promediada RGB",
                             "Cuasi Suma Clampeada YIQ", "Cuasi Suma Promediada YIQ",
                             "Cuasi Resta Clampeada YIQ", "Cuasi Resta Promediada YIQ",
                             "Producto de Imágenes", "Cociente de Imágenes", 
                             "Resta Valor Absoluto", "If Darker", "If Lighter")
operacionesMenu.grid(row=3, column=0, columnspan=2)

# Botón para procesar la imagen
procesarBtn = Button(ventana, text="Procesar Imagen", command=procesarImagen)
procesarBtn.grid(row=4, column=0, columnspan=3)

# Etiqueta para mostrar el resultado
resultadoLabel = Label(ventana, text="")
resultadoLabel.grid(row=5, column=0, columnspan=3)

ventana.mainloop()



