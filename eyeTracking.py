# https://github.com/octerry/Vox
# Code by Octerry
# Made On Earth By Humans

import cv2
# import numpy as np

max_cameras = 10
available = []
for i in range(max_cameras):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)

    if  cap.read()[0]:
        available.append(i)
        cap.release()

chosen = input(f"Numéro de votre caméra (entre 0 et {len(available)-1}): ") if len(available) > 1 else 0
print("chargement...")
webcam = cv2.VideoCapture(int(chosen))

ret, frame = webcam.read()
height, length = frame.shape[:2]
print(height, length)

# on créé une boucle
while(True):
    #on recupere frame par frame
    ret, frame = webcam.read()
    frame = frame[:,80:]

    _, threshold = cv2.threshold(frame, 40, 255, cv2.THRESH_BINARY_INV)

    # on affiche le frame
    cv2.imshow("threshold", threshold)
    cv2.imshow('frame', frame)

    #on dit au logiciel d'attendre que la touche "q" soit pressée pour arrêter >
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()