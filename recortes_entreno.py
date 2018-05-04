'Archivo que recorre las carpetas donde estan las fotografias de los tomates para sacarle una muestra'

from __future__ import division
import cv2
import numpy as np
from os import listdir

'Funcion de recorrido de carpetas'
#Recorre el directorio buscando las imagenes que 
def lecturaImagenes(directorio_entrada, directorio_salida, imagenes):
    for nombreImagen in imagenes:
        print nombreImagen
        #imagen = cv2.imread(directorio_entrada + "/" +nombreImagen)
        #Se encuentra el path de la imagen
        path = directorio_entrada + "/" + nombreImagen
        encontrarT = sacar_muestra(path)#Funcion que encuentra el tomate y saca la muestra
        cv2.imwrite(directorio_salida + "/" + nombreImagen, encontrarT)

#Saca la muestra de la imagen
#Retorna la foto 
def sacar_muestra(direccion_imagen):
    imagen = cv2.imread(direccion_imagen)#lee la imagen seleccionada
    #cv2.imshow('original', imagen)#muestra la imagen seleccionada
    imageng = cv2.GaussianBlur(imagen, (7,7), 0)#aplica el primer filtro de suavisado de la imagen con la funcion blur y gauss, los parametros son (imagen_original, tama;o de la matriz, mientras mas alto el valor mas suavizada estara, y de preferencia debe ser numero impar para poder posicionar el pixel en el centro, y 0 por defectoes la anchura de la campana de gauss))
    #cv2.imshow('suavizada',imageng)#muestra la imagen suavizada
    imagenc = cv2.Canny(imageng,50,150)#es la mascara que detecta bordes, la funcion canny convierte la imagen a blanco y negro y detecta todos los bordes,parametros(imagen_suavizada, umbral minimo, umbralmaximo))
    #cv2.imshow('bordeada', imagenc)# muestra imagen bordeada
    imagen_muestra = cv2.resize(imagen, (400,200))
    #cv2.imshow('imagen muestra',imagen_muestra)

    (_,contorno,_)= cv2.findContours(imagenc.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #funcion que encuentra el contorno en la imagen, parametros(copia_imagen_contorno, funcion_que_obtiene_el_contorno_exterior, funcion_que_elimina_puntos_redundantes)

    cv2.drawContours (imagen, contorno, -1, (0,255,0), 3)#dibuja contornos parametros(imagen_original, imagen_contorneada_, numero_de_contornos_, valoresbgr, numero_de_grosor_de_linea)
    t_contorno = [(cv2.contourArea(contor), contor) for contor in contorno]
    contorno_maximo = max(t_contorno, key= lambda x: x[0])[1]
    mask = np.zeros(imagen.shape, np.uint8)
    c_maximo = cv2.drawContours(mask, [contorno_maximo],-1, 255, -1)

    #centro del objeto
    centro = cv2.moments(contorno_maximo)
    cx = int(centro['m10']/centro['m00'])
    cy = int(centro['m01']/centro['m00'])
    print cx, cy
    dibujocentro = cv2.circle(mask, (cx,cy), 5 ,(0,0,255),3)
    #cv2.imshow('centro', dibujocentro)
    #cv2.imshow('contornos', imagen)
    muestra = imageng.copy()
    recorte = muestra[cy-50:cy+50, cx-50:cx+50]
    #cv2.imshow('muestra', recorte)
    cv2.waitKey(0)
    return(recorte)

def principal():
    #Lee las imagenes en las carpetas
    print "Tomates maduros"
    #lecturaImagenes("ImagenesTomates/TomateMaduro","Recortes/TomateMaduro",listdir("./ImagenesTomates/TomateMaduro"))
    print "Tomates Verdes"
    #lecturaImagenes("ImagenesTomates/TomateVerde","Recortes/TomateVerde",listdir("./ImagenesTomates/TomateVerde"))
    print "Tomates Podridos"
    lecturaImagenes("ImagenesTomates/TomatePodrido","Recortes/TomatePodrido",listdir("./ImagenesTomates/TomatePodrido"))
    #lecturaImagenes("Verde","Recortes/TomateVerde",listdir("./Verde"))

principal()
