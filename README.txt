Caracteristicas:
	Este software se basa en librerias de codigo abierto de Python como lo son openCV, NeuroLab, entre otras.
	El software cuenta con tres archivos de Python los cuales seran descritos acontinuación
	El software cuenta con tratamiento de imagenes, asi como una IA que determina el nivel de maduración, calidad y tiempo del tomate

Pasos para poder entrenar el software
	1. Se necesitan tener dos carpetas, adentro de la carpeta principal del proyecto.
		ImagenesTomates -> En la cual se necesita tener las imagenes clasificadas en tres subcarpetas, dependiendo del tipo de tomate
			./TomateMaduro
			./TomateVerde
			./TomatePodrido
			Tomates de nivel medio, pueden encontrarse en la carpeta de TomateMaduro o en la de TomateVerde
		RecortesTomates -> En esta carpeta se almacenaran las muestras que se agarraron de las imagenes que estan almacenadas en las carpetas anteriores.

	2. Una vez ordenado las imagenes se debe ejecutar, ya sea por medio de linea de comando o por sublime:
		recortes_entreno.py
		entrenamientoNeurolab.py -> Este archivo se debera ejecutar dos veces, la primera vez asegurandose que en la funcion main este de esta forma:
			def main():	
				GuardarArchivo()
				#EntrenamientoRNA()
		Luego la segunda vez que se ejecutara sera comentando la linea de arriba y descomentando la de abajo.
	3. Una vez eso, se creará un archivo llamado redEntrenada.net, el cual será la RNA ya entrenada lista para ser ejecutada

El software cuenta a su vez con una Interfaz Grafica de Usuario, con una RNA ya entrenada y lista para solo cargar una imagen y determinar el nivel de madurez de dicho tomate.

Para ello deberá ejecutar, ya sea por linea de comandos o por sublime el archivo:
	Principal.py

Se mostrara una ventana debera presionar el boton Abrir que se encuentra en la esquina superior derecha.
Luego seleccionar la imagen del tomate que desea analizar
Luego la IA empezará a trabajar y se le arrojará las salidas en la parte correspondiente

Y ¡Listo!
