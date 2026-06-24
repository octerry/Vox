import cv2
import numpy as np

max_cameras = 10
available = []
for i in range(max_cameras):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)

    if  cap.read()[0]:
        available.append(i)
        cap.release()

chosen = input(f"Numéro de votre caméra (entre 0 et {len(available)-1}): ") if len(available) > 1 else 0
webcam = cv2.VideoCapture(int(chosen))
# on créé une boucle

def increaseContrast(frame):
    # converting to LAB color space
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Load image in grayscale
    gray_minus = np.clip(frame-100, 0, 255).astype(np.uint8)
    gray_plus = np.clip(frame+100, 0, 255).astype(np.uint8)

    result = cv2.hconcat([frame, gray_minus, gray_plus])

    # # Applying CLAHE to L-channel
    # # feel free to try different values for the limit and grid size:
    # clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(8, 8))
    # cl = clahe.apply(l_channel)
    #
    # # merge the CLAHE enhanced L-channel with the a and b channel
    # limg = cv2.merge((cl, a, b))
    #
    # # Converting image from LAB Color model to BGR color spcae
    # enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Stacking the original image with the enhanced image
    # result = np.hstack((frame, enhanced_img))
    return result

while(True):
    #on recupere frame par frame
    ret, frame = webcam.read()
    hauteur, largeur, couleurs = frame.shape

    print(largeur, hauteur)

    maxPosition = None
    maxColorSum = 0

    print(min(frame.flatten()))

    contrastedFrame = increaseContrast(frame)

    # on affiche le frame
    cv2.imshow('frame', contrastedFrame)
    #on dit au logiciel d'attendre que la touche "q" soit pressée pour arrêter >
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()