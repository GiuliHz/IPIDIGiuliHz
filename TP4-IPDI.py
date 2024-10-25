import tkinter as tk
from tkinter import filedialog, Label, Button, OptionMenu, StringVar
from PIL import Image, ImageTk
import numpy as np

# Funciones morfológicas
def erosion(imagen):
    return aplicar_operacion_morfologica(imagen, np.min)

def dilatacion(imagen):
    return aplicar_operacion_morfologica(imagen, np.max)

def apertura(imagen):
    return dilatacion(erosion(imagen))

def cierre(imagen):
    return erosion(dilatacion(imagen))

def borde_morfologico_externo(imagen):
    imagen_dilatada = dilatacion(imagen)  
    imagen_dilatada_np = np.array(imagen_dilatada)  # Convertir a arreglo NumPy
    imagen_original_np = np.array(imagen.convert("L"))  # Asegurarse de que la imagen esté en escala de grises

    # Calcular el borde exterior restando la imagen original de la dilatada
    nueva_imagen = np.clip(imagen_dilatada_np - imagen_original_np, 0, 255)  # Asegura que los valores estén en el rango 0-255
    return Image.fromarray(nueva_imagen.astype(np.uint8))  # Asegúrate de que los valores son del tipo adecuado
def borde_morfologico_interno(imagen):
   
    imagen_dilatada = erosion(imagen)  
    imagen_dilatada_np = np.array(imagen_dilatada)  # Convertir a arreglo NumPy
    imagen_original_np = np.array(imagen.convert("L"))  # Asegurarse de que la imagen esté en escala de grises

    # Calcular el borde exterior restando la imagen original de la dilatada
    nueva_imagen = np.clip(imagen_original_np - imagen_dilatada_np, 0, 255)  # Asegura que los valores estén en el rango 0-255
    return Image.fromarray(nueva_imagen.astype(np.uint8))  # Asegúrate de que los valores son del tipo adecuado

def mediana(imagen):
    return aplicar_operacion_morfologica(imagen, np.median)

def aplicar_operacion_morfologica(imagen, operacion):
    imagen_np = np.array(imagen)
    nueva_imagen = np.zeros_like(imagen_np)
    for x in range(1, imagen_np.shape[0]-1):
        for y in range(1, imagen_np.shape[1]-1):
            vecindad = imagen_np[x-1:x+2, y-1:y+2]
            nueva_imagen[x, y] = operacion(vecindad)
    return Image.fromarray(nueva_imagen.astype(np.uint8))

# Interfaz gráfica
class AplicacionFiltros:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtros Morfológicos")
        
        self.imagen_original = None
        self.imagen_filtrada = None

        # Cargar imagen
        self.label_imagen_original = Label(root, text="Imagen Original")
        self.label_imagen_original.grid(row=0, column=0)

        self.label_imagen_filtrada = Label(root, text="Imagen Filtrada")
        self.label_imagen_filtrada.grid(row=0, column=2)

        self.boton_cargar = Button(root, text="Cargar", command=self.cargar_imagen)
        self.boton_cargar.grid(row=2, column=0)

        # Crear botón Filtrar
        self.boton_filtrar = Button(root, text="Filtrar ->", command=self.aplicar_filtro)
        self.boton_filtrar.grid(row=1, column=1)

        # Crear botón Copiar
        self.boton_copiar = Button(root, text="<- Copiar", command=self.copiar_imagen)
        self.boton_copiar.grid(row=2, column=1)

        # Crear botón Guardar
        self.boton_guardar = Button(root, text="Guardar", command=self.guardar_imagen)
        self.boton_guardar.grid(row=2, column=2)

        # Menú desplegable para filtros
        self.filtro_var = StringVar(root)
        self.filtro_var.set("Erosión")
        opciones_filtros = ["Erosión", "Dilatación", "Apertura", "Cierre", "Borde Morfológico Externo","Borde Morfológico Interno", "Mediana"]
        self.menu_filtros = OptionMenu(root, self.filtro_var, *opciones_filtros)
        self.menu_filtros.grid(row=3, column=1)

    def cargar_imagen(self):
        archivo = filedialog.askopenfilename()
        if archivo:
            self.imagen_original = Image.open(archivo).convert('L')
            self.mostrar_imagen(self.imagen_original, 0)

    def mostrar_imagen(self, imagen, columna):
        imagen_resized = imagen.resize((150, 150))
        imagen_tk = ImageTk.PhotoImage(imagen_resized)
        label_imagen = Label(self.root, image=imagen_tk)
        label_imagen.image = imagen_tk
        label_imagen.grid(row=1, column=columna)

    def aplicar_filtro(self):
        if self.imagen_original:
            filtro = self.filtro_var.get()
            if filtro == "Erosión":
                self.imagen_filtrada = erosion(self.imagen_original)
            elif filtro == "Dilatación":
                self.imagen_filtrada = dilatacion(self.imagen_original)
            elif filtro == "Apertura":
                self.imagen_filtrada = apertura(self.imagen_original)
            elif filtro == "Cierre":
                self.imagen_filtrada = cierre(self.imagen_original)
            elif filtro == "Borde Morfológico Externo":
                self.imagen_filtrada = borde_morfologico_externo(self.imagen_original)
            elif filtro == "Borde Morfológico Interno":
                self.imagen_filtrada = borde_morfologico_interno(self.imagen_original)      
            elif filtro == "Mediana":
                self.imagen_filtrada = mediana(self.imagen_original)

            self.mostrar_imagen(self.imagen_filtrada, 2)

    def copiar_imagen(self):
        if self.imagen_filtrada:
            self.imagen_original = self.imagen_filtrada
            self.mostrar_imagen(self.imagen_original, 0)

    def guardar_imagen(self):
        if self.imagen_filtrada:
            archivo = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if archivo:
                self.imagen_filtrada.save(archivo)

# Crear ventana principal
root = tk.Tk()
app = AplicacionFiltros(root)
root.mainloop()

