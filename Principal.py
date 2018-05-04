#Librerias para la la creacion de la interfaz
from __future__ import division
import cv2
import numpy as np
from os import listdir
import os
import neurolab as nl
import scipy as sp
import cPickle as pickle
import dill
from Tkinter import *
from PIL import Image, ImageTk
from Tkinter import Tk, Label, BOTH, RAISED, RIGHT
from ttk import Frame, Style, Button
from tkFileDialog import askopenfilename

#Interfaz
class Interfaz(Frame):
	#muestra tkflied para abrir un archivo
    #guarda la ruta del archivo
	def abrirCuadro(self):
		Tk().withdraw()
		nombreImagen = askopenfilename()
		self.IA(nombreImagen)#Inicia la IA a analizar el tomate
		self.mostrarImagen(nombreImagen)#se muestra la imagen

    #Carga la imagen que se selecciono en pantalla
	def mostrarImagen(self, filename):
		bard = Image.open(filename)
		bard = bard.resize((300,300), Image.ANTIALIAS)
		bardejov = ImageTk.PhotoImage(bard)
		label1 = Label(self, image=bardejov)
		label1.image = bardejov
		label1.place(x=550, y=150)

	#Constructor
	def __init__(self, parent1):
		Frame.__init__(self, parent1)
		self.parent = parent1
		self.initUI()

	#Madurez del tomate
	def salida1(self, texto):
		label = Label(self, text=texto, fg="#ffff00", bg="#333", font = "Helvetica 16 bold italic")
		label.place(x=250, y=200)

	#Calidad del Tomate
	def salida2(self, texto):
		label = Label(self, text=texto, fg="#ffff00", bg="#333", font = "Helvetica 16 bold italic")
		label.place(x=250, y=300)

	#Tiempo del Tomate
	def salida3(self, texto):
		label = Label(self, text=texto, fg="#ffff00", bg="#333", font = "Helvetica 16 bold italic")
		label.place(x=250, y=400)

	def initUI(self):
		self.parent.title("IA Tomates")
		self.pack(fill=BOTH, expand=True)
		Style().configure("TFrame", background="#00008B")
		# self.imagen("inicio.jpg")
		self.salida1("")
		self.salida2("")
		self.salida3("")

		AbrirButton = Button(self, text="Abrir")
		AbrirButton.pack(side=RIGHT, padx=5, pady=5)
		AbrirButton.place(x=50, y=25)
		AbrirButton["command"] = self.abrirCuadro

		label = Label(self, text="TOMATO ANALYZER", fg="#DF0101", bg="#00008B", font = "Arial 24")
		label.place(x=300, y=25)
		label = Label(self, text="Informacion del Tomate:", fg="#FFFFFF", bg="#00008B", font = "Arial 20")
		label.place(x=100, y=100)

		label = Label(self, text="Nivel de Madurez:", fg="#FFFFFF", bg="#00008B", font = "Arial 14")
		label.place(x=50, y=200)
		label = Label(self, text="Calidad del Tomate:", fg="#FFFFFF", bg="#00008B", font = "Arial 14")
		label.place(x=50, y=300)
		label = Label(self, text="Tiempo de Consumo:", fg="#FFFFFF", bg="#00008B", font = "Arial 14")
		label.place(x=50, y=400)

	#Tratamiento de imagenes 
	#Esto es para antes de la IA
	def sacar_muestra(self,direccion_imagen):
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

	def normalizar(self,valor):
		salida = (valor*1.)/255.
		return salida

	def obtenerPixels(self,imagen):
		#se abre la imagen
		im = Image.open(imagen)
		im = im.resize((30, 30), Image.ANTIALIAS)

		pixels = im.load()
		filas, columnas = im.size
		decimales = 4
		cadena = ""
		for columna in range (columnas):
			for fila in range(filas):
				#se separan los valores RGB y se escriben en el archivo
				rojo = str(self.normalizar(pixels[fila,columna][0]))
				verde = str(self.normalizar(pixels[fila,columna][1]))
				azul = str(self.normalizar(pixels[fila,columna][2]))
				cadena = cadena + rojo[:rojo.find(".")+decimales] + " " + verde[:verde.find(".")+decimales] + " " + azul[:azul.find(".")+decimales] + " "

		return cadena

	#Una vez obtenida la imagen, se pasa por la IA
	def IA(self,path):
		#tratamiento de la imagen
		imagenOriginal = cv2.imread(path)
		imagenMuestra = self.sacar_muestra(path)#saca la muestra de la imagen
		cv2.imwrite("muestraTomate.jpg",imagenMuestra)#Se guarda la muestra para luego sacarla
		datitos =  self.obtenerPixels("muestraTomate.jpg")#Cambiar nombre de funcion
		#Se elimina el archivo si existe
		if(os.path.exists("archivoEntrada.csv")== True):
			os.remove("archivoEntrada.csv")

		#Se crea el archivo y se le pasa los datos ya normalizados, luego se cierra
		entradas = open("archivoEntrada.csv", "a")
		entradas.write(datitos)
		entradas.close()
		#Se cargan los datos, ya normalizados, para meter a la IA
		datosEntrada = np.matrix(sp.genfromtxt("archivoEntrada.csv", delimiter=" "))
		red_neuronal = nl.load("redEntrenada.net")#Se carga el archivo de entrenamiento.
		salidaRed = red_neuronal.sim(datosEntrada)#Aca se ejecuta la red neuronal

		#Se cara un porcentaje de la RNA para ver el nivel de de categoria que se tiene
		#Esto con el fin de determinar el tiempo que lleva-o falta el tomate en ese estado
		TomateMaduro = salidaRed[0][1]*100
		TomatePodrido = salidaRed[0][0]*100
		TomateVerde = salidaRed[0][2]*100

		print "Salida Maduro " , TomateMaduro
		print "Salida Podrido ", TomatePodrido
		print "Salida Verde " , TomateVerde

		if (TomateMaduro>TomatePodrido) and (TomateMaduro>TomateVerde):
		#Tomate maduro
			self.salida1("Maduro")
			#Condiciones para determinar el tiempo de consumo del tomate
			if (TomatePodrido < -20):
				self.salida2("Calidad Alta")
				self.salida3("6 dias de consumo")
			elif (TomatePodrido < 0):
				self.salida2("Calidad Alta")
				self.salida3("4 dias de consumo")
			elif (TomatePodrido < 20):
				self.salida2("Calidad Media")
				self.salida3("2 dias para consumo")
			elif (TomatePodrido< 40):
				self.salida2("Calidad Baja")
				self.salida3("1 dia para consumo")
			else:
				self.salida2("Calidad Mala")
				self.salida3("El tomate esta a punto de podrirse")

		elif (TomateVerde>TomatePodrido) and (TomateVerde>TomateMaduro):
			#Tomate Verde
			#Calidad del tomate
			if (TomatePodrido < - 20):
				self.salida2("Calidad Alta")
			elif (TomatePodrido < 10):
				self.salida2("Calidad Media")
			elif (TomatePodrido < 30):
				self.salida2("Calidad Mala")
			self.salida1("Verde")#Nivel de madurez que se tiene
			#Tiempo para maduracion
			if (TomateMaduro< 1 ):
			#Esta muy verde
				self.salida3("15 dias para madurar")
			elif (TomateMaduro<3):
				self.salida3("9 dias para madurar")
			elif (TomateMaduro>3):
				self.salida3("4 dias para madurar")
			if (TomatePodrido>5):
				self.salida3("4 dias para madurar")
		elif (TomatePodrido>TomateMaduro) and (TomatePodrido>TomateVerde):
			#Tomate Podrido
			self.salida1("Podrido")
			self.salida2("Mala Calidad :(")
			self.salida3("Tiempo expirado :(")
		else:
			#Error
			self.salida1("No se reconoce :(")
			self.salida2("No se reconoce :(")
			self.salida3("No se reconoce :(")


#Fin clase
def main():
	root = Tk()
	root.geometry("900x500")
	root.resizable(False,False)
	app = Interfaz(root)
	root.mainloop()

main()
