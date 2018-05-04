#Librerias a necesitar
import neurolab as nl
import numpy as np
import scipy as sp
import pylab as pl
from PIL import Image
from os import listdir
import os

#Funcion para normalizar, ya que los pixeles iran de 0-255
def normalizar(valor):
	salida = (valor*1.)/255.
	return salida

#Del archivo de las entradas obtiene los datos para normalizarlos	
def obtenerPixels(path, salidas):
    #se abre la imagen
    imagen = Image.open(path)
    #redimensiona la imagen.
    imagen = imagen.resize((30, 30), Image.ANTIALIAS)#o de 40*10

    pixels = imagen.load()

    #se abre el archivo con los datos para el entrenamiento
    archivo = open("datos.csv", "a")
    fil, column = imagen.size
    decimales = 4
    for columna in range (column):
        for fila in range(fil):
            #se separan los valores RGB y se escriben en el archivo
            r = str(normalizar(pixels[fila,columna][0]))
            g = str(normalizar(pixels[fila,columna][1]))
            b = str(normalizar(pixels[fila,columna][2]))
            #cadena contendra los valores rgb separados por espacio
            cadena = r[:r.find(".")+decimales] + " " + g[:g.find(".")+decimales] + " " + b[:b.find(".")+decimales] + " "
            archivo.write(cadena)

 	#Se escribe en el archivo y se cierra
    archivo.write(salidas)
    archivo.write("\n")
    archivo.close()

#Esta funcion es la principal a lahora de hacer la normalizacion.
def GuardarArchivo():
	#en caso de que exista el archivo, eliminar dicho archivo
	#datos.csv es donde se encuentran los datos de entrenamiento, de entrada y de salida
	if(os.path.exists("datos.csv")== True):
		os.remove("datos.csv")
	obtenerImagenes("Recortes/TomateMaduro", listdir("./Recortes/TomateMaduro"), "0 1 0")
	obtenerImagenes("Recortes/TomatePodrido",  listdir("./Recortes/TomatePodrido"), "1 0 0")
	obtenerImagenes("Recortes/TomateVerde", listdir("./Recortes/TomateVerde"), "0 0 1" )

#Funcion que recorre todas las imagenes de la carpeta enviada, segun sea el tipo de tomate
def obtenerImagenes(carpeta_entrada, lista_imagenes, salida):
    for nombre_imagen in lista_imagenes:
        print nombre_imagen
        obtenerPixels(carpeta_entrada + "/" +nombre_imagen, salida)

#Funcion principal donde realiza el entrenamiento la red.
def EntrenamientoRNA():
	#Lee el archivo que contiene los datos ya normalizados para la red
	datos = np.matrix(sp.genfromtxt("datos.csv", delimiter=" "))
	#Numero de salidas de la neurona
	columanas_salida = 3

	#datos de entrada para la neurona
	entrada = datos[:,:-3]

	#datos de salida para la neurona
	salidas = datos[:,-3:]

	print "Entradas"
	print entrada

	print "Salidas"
	print salidas
	#max min para cada dato de entrada a la neurona 
	maxMin = np.matrix([[ -5, 5] for i in range(len(entrada[1,:].T))])

	# valores para las capas de la neurona 
	capa1 = entrada.shape[0]
	capa2 = int(capa1*0.5)  #El numero de neuronas sera la mitad que de la capa1
	capa3 = int(capa1*0.33) #El numero de neuronas sera un tercio de la capa1
	capa4 = 3 # Las salidas seran los tres niveles de madurez y un error

	# Crear red neuronal con 4 capas 1 de entrada 2 ocultas y 1 de salida 
	red_neuronal = nl.net.newff(maxMin, [capa1,capa2,capa3,capa4])

	#El algoritmo sera el backpropagation
	red_neuronal.trainf = nl.train.train_gd

	#Datos para la RNAd
	#0.02 sera el error minimo
	error = red_neuronal.train(entrada, salidas, epochs=7500000, show=1000, goal=0.2, lr=0.01)

	#Luego de que este entrenada, se guardara en la misma carpeta donde se encuentre este archivo
	#Con el nombre de redEntrenada
	#.net sera la extension del archivo
	graficar(error)
	red_neuronal.save("redEntrenada.net")
	salida = red_neuronal.sim(entrada)
	print salida
#Fin funcion entrenamiento
def graficar(error):
	pl.plot(error)
	pl.xlabel('Epoca number')
	pl.ylabel('Error')
	pl.grid()
	pl.show()

#Funcion principal del programa
#Esta funcion llama a las dos mas importantes
#Para normalizar las imagenes primero y luego entrenar
def main():
	#De primero se debe llamar a GuardarArchivo
	#una vez eso se comenta y se llama a EntrenamientoRNA
	#GuardarArchivo()
	EntrenamientoRNA()

main()