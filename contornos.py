import cv2
import numpy as np

imagen = cv2.imread('tomate1.jpg')#lee la imagen seleccionada
cv2.imshow('original', imagen)#muestra la imagen seleccionada
imageng = cv2.GaussianBlur(imagen, (7,7), 0)#aplica el primer filtro de suavisado de la imagen con la funcion blur y gauss, los parametros son (imagen_original, tama;o de la matriz, mientras mas alto el valor mas suavizada estara, y de preferencia debe ser numero impar para poder posicionar el pixel en el centro, y 0 por defectoes la anchura de la campana de gauss))
cv2.imshow('suavizada',imageng)#muestra la imagen suavizada
imagenc = cv2.Canny(imageng,50,150)#es la mascara que detecta bordes, la funcion canny convierte la imagen a blanco y negro y detecta todos los bordes,parametros(imagen_suavizada, umbral minimo, umbralmaximo))
cv2.imshow('bordeada', imagenc)# muestra imagen bordeada



(_,contorno,_)= cv2.findContours(imagenc.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#funcion que encuentra el contorno en la imagen, parametros(copia_imagen_contorno, funcion_que_obtiene_el_contorno_exterior, funcion_que_elimina_puntos_redundantes)

cv2.drawContours (imagen, contorno, -1, (0,255,0), 3)#dibuja contornos parametros(imagen_original, imagen_contorneada_, numero_de_contornos_, valoresbgr, numero_de_grosor_de_linea)
cv2.imshow('contornos', imagen)
muestra = imagen.copy()
recorte = muestra[10:200, 50:150]
cv2.imshow('muestra', recorte)
cv2.waitKey(0)
 

