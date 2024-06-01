 # en este modulo se colocan los efectos de quitar el fondo y deteccion de bordes
# tambien esta la fusion de frames/imagenes
import cv2 as cv
import numpy as np

# BGR
COLOR_BORDES = (213, 46, 130)

# Parametros para Canny 
# (se hicieron pruebas y con estos se tenia una mejor visualizacion)
LIMITE_INF = 80
LIMITE_SUP = 160

# Parámetros para aplicar la Dilatación
TAMANO_KERNEL = 3
elemento = cv.getStructuringElement(cv.MORPH_CROSS, (TAMANO_KERNEL, TAMANO_KERNEL))


def removeBackgroud(frame):
    # El codigo para remover el fondo fue tomado de:
    # https://stackoverflow.com/questions/51719472/remove-green-background-screen-from-image-using-opencv-python
    
    # suavizado para reduccion de ruido
    frame = cv.GaussianBlur(frame, (5,5), sigmaX=3, sigmaY=3, borderType = cv.BORDER_DEFAULT)
    # se usa el espacio de color LAB
    lab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
    
    # se extrae el canal A
    A = lab[:,:,1]

    thresh = cv.threshold(A, 127, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)[1]

    mascara = cv.bitwise_and(frame, frame, mask=thresh)

    mask1 = mascara.copy()

    mask1[thresh == 0] =(255,255,255)

    mask_lab = cv.cvtColor(mascara, cv.COLOR_BGR2LAB)

    frame_destino = cv.normalize(mask_lab[:,:,1], dst=None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)

    frame_destino_thresh = cv.threshold(frame_destino, 100, 255, cv.THRESH_BINARY_INV)[1]


    mask_lab[:,:,1][frame_destino_thresh == 255] = 127

    resultado = cv.cvtColor(mask_lab,cv.COLOR_LAB2BGR)

    resultado[thresh == 0] = (255,255,255)

    return resultado


def bordesColor(frame):
    # SE CONVIERTE A ESCALA DE GRISES PARA EL DETECTOR DE BORDES
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    frame_suave = cv.GaussianBlur(frame_gray, (5,5), 0)

    bordes = cv.Canny(frame_suave, LIMITE_INF, LIMITE_SUP)

    # se dilatan los bordes para mejor visualizacion

    bordes = cv.dilate(bordes, elemento)

    # agrego color a los bordes

    bordes_de_color = cv.cvtColor(bordes, cv.COLOR_BGR2RGB)

    imagen_resultado = np.zeros_like(bordes_de_color)

    # se escogen solo los bordes, pixeles mayores a cero
    mask = bordes > 0

    imagen_resultado[mask] = COLOR_BORDES

    return imagen_resultado


