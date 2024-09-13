import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def rgbAyiq(rgb):
    """Convierte un array de colores RGB a YIQ."""
    yiq = np.dot(rgb, [[0.299, 0.587, 0.114],
                       [0.5957, -0.2744, -0.3213],
                       [0.2115, -0.5226, 0.3111]])
    return yiq

def yiqArgb(yiq):
    """Convierte un array de colores YIQ a RGB."""
    rgb = np.dot(yiq, [[1, 0.9563, 0.6210],
                       [1, -0.2721, -0.6474],
                       [1, -1.1070, 1.7046]])
    return rgb

def ajustarLuminanciaSaturacion(imagen, coefLuminancia=1.0, coefSaturacion=1.0):
    """Ajusta la luminancia y saturación de la imagen, manejando imágenes con canal alfa."""
    # Convertir imagen a array y normalizar valores de RGB
    arrayImagen = np.asarray(imagen) / 255.0
    # Si la imagen tiene un canal alfa, sepáralo
    if arrayImagen.shape[-1] == 4:
        arrayRgb = arrayImagen[..., :3]  # Excluye el canal alfa
        canalAlpha = arrayImagen[..., 3]  # Guarda el canal alfa para después
    else:
        arrayRgb = arrayImagen
    
    # Convertir de RGB a YIQ
    yiq = rgbAyiq(arrayRgb)
    
    # Ajustar luminancia y saturación
    yiq[..., 0] *= coefLuminancia  # Ajuste de luminancia
    yiq[..., 1] *= coefSaturacion  # Ajuste de satugit commitración en I
    yiq[..., 2] *= coefSaturacion  # Ajuste de saturación en Q
    
    # Asegurarse de que los valores están en el rango permitido
    yiq[..., 0] = np.clip(yiq[..., 0], 0, 1)
    yiq[..., 1] = np.clip(yiq[..., 1], -0.5957, 0.5957)
    yiq[..., 2] = np.clip(yiq[..., 2], -0.5226, 0.5226)
    
    # Convertir de YIQ a RGB
    rgb = yiqArgb(yiq)
    
    # Convertir de vuelta a rango de bytes (0-255)
    rgb = np.clip(rgb * 255, 0, 255).astype(np.uint8)
    
    # Si la imagen original tenía un canal alfa, agrégalo de nuevo
    if arrayImagen.shape[-1] == 4:
        rgb = np.dstack((rgb, (canalAlpha * 255).astype(np.uint8)))

    return Image.fromarray(rgb)

# Cargar una imagen
imagen = Image.open("C:/Users/Gustavo Nelles/Pictures/ultima final.jpg")

# Ajustar luminancia y saturación
coefLuminancia = 1  # Coeficiente de luminancia
coefSaturacion = 0 # Coeficiente de saturación
imagenProcesada = ajustarLuminanciaSaturacion(imagen, coefLuminancia, coefSaturacion)

# Mostrar la imagen original y la procesada
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Imagen Original")
plt.imshow(imagen)

plt.subplot(1, 2, 2)
plt.title("Imagen Procesada")
plt.imshow(imagenProcesada)

plt.show()

