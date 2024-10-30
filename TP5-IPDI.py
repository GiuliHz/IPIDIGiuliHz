import numpy as np

from tkinter import Tk, Button, Menu, filedialog, Label, Frame, Canvas
from PIL import Image, ImageTk


def binarizacion50(img):
    umral = np.median(img)
    bin_img = np.where(img > umral, 1, 0)
    return bin_img

def binarizacionModas(img):
    hist, _ = np.histogram(img, bins=256, range=(0, 1))
    moda_clara, moda_oscura = np.argmax(hist[:128]), np.argmax(hist[128:]) + 128
    umbral = (moda_clara + moda_oscura) / 255
    bin_img = np.where(img > umbral, 1, 0)
    return bin_img

def binarizacionOtsu(img):
    pixel_numb = img.size
    prom_pond = 1 / pixel_numb
    hist, _ = np.histogram(img, bins=100, range=(0, 1))
    final_thresh, final_value = -1, -1
    intensity = np.arange(100)
    for x in range(1, 100):
        pcb, pcf = np.sum(hist[:x]), np.sum(hist[x:])
        wb, wf = pcb * prom_pond, pcf * prom_pond
        mub = np.sum(intensity[:x] * hist[:x]) / pcb
        muf = np.sum(intensity[x:] * hist[x:]) / pcf
        value = wb * wf * (mub - muf) ** 2
        if value > final_value:
            final_thresh, final_value = x / 100, value
    bin_img = np.where(img > final_thresh, 1, 0)
    return bin_img

def filtroLaplaciano(img):
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
    return aplicarFiltro(img, kernel)

def erosion(imagen):
    return aplicar_operacion_morfologica(imagen, np.min)

def dilatacion(imagen):
    return aplicar_operacion_morfologica(imagen, np.max)

def aplicar_operacion_morfologica(imagen, operacion):
    imagen_np = np.array(imagen)
    nueva_imagen = np.zeros_like(imagen_np)
    for x in range(1, imagen_np.shape[0]-1):
        for y in range(1, imagen_np.shape[1]-1):
            vecindad = imagen_np[x-1:x+2, y-1:y+2]
            nueva_imagen[x, y] = operacion(vecindad)
    return nueva_imagen

def borde_morfologico_externo(imagen):
    imagen_dilatada = dilatacion(imagen)  
    imagen_dilatada_np = np.array(imagen_dilatada)  # Convertir a arreglo NumPy
    nueva_imagen = np.clip(imagen_dilatada_np - imagen, 0, 255)  # Asegura que los valores estén en el rango 0-255
    return nueva_imagen  # Asegúrate de que los valores son del tipo adecuado

def borde_morfologico_interno(imagen):
    imagen_dilatada = erosion(imagen)  
    imagen_dilatada_np = np.array(imagen_dilatada)  # Convertir a arreglo NumPy
    nueva_imagen = np.clip(imagen - imagen_dilatada_np, 0, 255)  # Asegura que los valores estén en el rango 0-255
    return nueva_imagen  # Asegúrate de que los valores son del tipo adecuado

def marchingSquares(img, threshold=0.5):
    bin_img = np.where(img > threshold, 1, 0)
    # Implementación básica para mostrar celdas
    return bin_img  # Para una visualización simple

def varitaMagica(img, semilla, tolerancia=0.1):
    x, y = semilla
    target_color = img[x, y]
    filled = np.zeros_like(img)
    frontera = [(x, y)]
    while frontera:
        x, y = frontera.pop()
        if filled[x, y] == 0 and abs(img[x, y] - target_color) < tolerancia:
            filled[x, y] = 1
            if x > 0: frontera.append((x - 1, y))
            if x < img.shape[0] - 1: frontera.append((x + 1, y))
            if y > 0: frontera.append((x, y - 1))
            if y < img.shape[1] - 1: frontera.append((x, y + 1))
    return filled

def aplicarFiltro(img, filtro):
    salida = np.zeros_like(img)
    padded = np.pad(img, pad_width=1, mode='edge')
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = padded[i:i + 3, j:j + 3]
            salida[i, j] = np.sum(region * filtro)
    return np.clip(salida, 0, 1)
# Funciones de carga, guardado y procesamiento
def cargarImagen(slot):
    archivo = filedialog.askopenfilename()
    if archivo:
        imagen = Image.open(archivo).convert('L')
        imagen = np.array(imagen) / 255.0
        if slot == 1:
            global img1_original, img1_procesada
            img1_original = imagen
            img1_procesada = imagen.copy()
            mostrarImagen(img1_procesada, canvas1)
        else:
            global img2_original, img2_procesada
            img2_original = imagen
            img2_procesada = imagen.copy()
            mostrarImagen(img2_procesada, canvas2)

def guardarImagen(slot):
    archivo = filedialog.asksaveasfilename(defaultextension=".png")
    if archivo:
        if slot == 1 and img1_procesada is not None:
            img = Image.fromarray((img1_procesada * 255).astype(np.uint8))
            img.save(archivo)
        elif slot == 2 and img2_procesada is not None:
            img = Image.fromarray((img2_procesada * 255).astype(np.uint8))
            img.save(archivo)

def mostrarImagen(imagen, canvas):
    imagen_pil = Image.fromarray((imagen * 255).astype(np.uint8))
    imagen_tk = ImageTk.PhotoImage(imagen_pil.resize((400, 400)))
    canvas.create_image(0, 0, anchor="nw", image=imagen_tk)
    canvas.imagen = imagen_tk

# Funciones de interfaz gráfica

def aplicarFiltroSeleccionado(slot, tipo):
    global img1_procesada, img2_procesada
    img_original = img1_original if slot == 1 else img2_original  # Obtiene la imagen original

    if tipo == "50% píxeles negros y blancos":
        img_procesada = binarizacion50(img_original)
    elif tipo == "Modas clara/oscura":
        img_procesada = binarizacionModas(img_original)
    elif tipo == "Otsu":
        img_procesada = binarizacionOtsu(img_original)
    elif tipo == "Laplaciano":
        img_procesada = filtroLaplaciano(img_original)
    elif tipo =="Borde morfológico externo":
        img_procesada = borde_morfologico_externo(img_original)
    elif tipo == "Borde morfológico interno":
        img_procesada = borde_morfologico_interno(img_original)
    elif tipo == "Marching Squares":
        img_procesada = marchingSquares(img_original)
    elif tipo == "Varita mágica":
        img_procesada = varitaMagica(img_original, (50, 50))  # Coordenada inicial arbitraria
    # Actualiza la imagen procesada sin modificar la original
    if slot == 1: 
        img1_procesada = img_procesada
        mostrarImagen(img1_procesada, canvas1)
    else:
        img2_procesada = img_procesada
        mostrarImagen(img2_procesada, canvas2)


# Crear la ventana de la interfaz
ventana = Tk()
ventana.title("Procesamiento de Imágenes")
ventana.geometry("1000x500")

# Contenedor y Canvas para las dos imágenes
frameIzq, frameDer = Frame(ventana), Frame(ventana)
frameIzq.grid(row=0, column=0), frameDer.grid(row=0, column=1)

canvas1 = Canvas(frameIzq, width=400, height=400)
canvas1.pack()
canvas2 = Canvas(frameDer, width=400, height=400)
canvas2.pack()

# Menú desplegable de filtros para cada imagen
menuFiltros1 = Menu(ventana, tearoff=0)
menuFiltros2 = Menu(ventana, tearoff=0)
tiposFiltros = ["50% píxeles negros y blancos", "Modas clara/oscura", "Otsu", "Laplaciano","Borde morfológico interno", "Borde morfológico externo", "Marching Squares", "Varita mágica"]
for tipo in tiposFiltros:
    menuFiltros1.add_command(label=tipo, command=lambda t=tipo: aplicarFiltroSeleccionado(1, t))
    menuFiltros2.add_command(label=tipo, command=lambda t=tipo: aplicarFiltroSeleccionado(2, t))

btnFiltros1 = Button(ventana, text="Filtros", command=lambda: menuFiltros1.post(btnFiltros1.winfo_rootx(), btnFiltros1.winfo_rooty()))
btnFiltros1.grid(row=2, column=0)
btnFiltros2 = Button(ventana, text="Filtros", command=lambda: menuFiltros2.post(btnFiltros2.winfo_rootx(), btnFiltros2.winfo_rooty()))
btnFiltros2.grid(row=2, column=1)

# Botones de carga y guardado
Button(ventana, text="Cargar", command=lambda: cargarImagen(1)).grid(row=1, column=0)
Button(ventana, text="Cargar", command=lambda: cargarImagen(2)).grid(row=1, column=1)
Button(ventana, text="Guardar", command=lambda: guardarImagen(1)).grid(row=3, column=0)
Button(ventana, text="Guardar", command=lambda: guardarImagen(2)).grid(row=3, column=1)

ventana.mainloop()


