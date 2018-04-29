import cv2
import numpy as np

img = np.zeros((512,512,3), np.uint8)
cv2.line(img,(0,0),(511,511),(255,0,0),5)
cv2.circle(img,(200,200), 15, (0,0,255), 3)
#parametros para circulo cv2.circle(imagen,(posicionx,posiciony),radio,(color en rgb), grosor de la linea'en -1 se rellena el circulo)
cv2.imshow('prueba',img)
cv2.waitKey(0)

