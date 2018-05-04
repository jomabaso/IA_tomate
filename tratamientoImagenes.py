from __future__ import division
import cv2
import numpy as np
from os import listdir

#Esta funcion recorrera la carpeta de entrada la cual es la de ImagenesTomates
#Para trabajarlas con openCV
#	Que encntrara el tomate para despues sacar una muestra de preferencia mas grande que 50*20
#	Tambien se hara un suavizado a la imagen
#	Por ultimo se guardara en la carpeta de salida que es la de Recortes
def lecturaImagenes(directorio_entrada, directorio_salida, imagenes):
    for nombreImagen in imagenes:
        print nombreImagen
        imagen = cv2.imread(directorio_entrada + "/" +nombreImagen)
        #Aca se debe poner las funciones de jorge
        encontrarT = ecnontrar_tomate(imagen)#Funcion que encuentra el tomate
        cv2.imwrite(directorio_salida + "/" + nombreImagen, encontrarT)
