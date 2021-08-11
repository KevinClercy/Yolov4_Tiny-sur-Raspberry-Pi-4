import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from SendCoordonneV2 import *
import struct
from smbus import SMBus
import time

'''
Ce programme permet de détecter des personnes ainsi que des objets dangeureux avec OpenCV
et d'un modèle custom. Quand un objet dangereux est detecté, une notification est envoyé.
La position de la personne est aussi envoyé via I2C sur un Arduino pour gerer la position de
la caméra afin de conserver la personne au centre de l'image.

Rédigé par K. Clercy, R. Lupien et M. Le Vergos
PFE2021
Avr. 2021
Aou. 2021

Partie envoie de notification
Rédigé par T. Wong
GPA788
Jan. 2019
Aut. 2020

Modifié par K. Clercy
PFE2021
Avr. 2021
Aou. 2021
'''
# Importer la classe Envoi_Courriel
from gpa788_envoi_courriel import Envoi_Courriel
import smtplib
import Parametres

#### Load YOLO
net = cv2.dnn.readNet ( Parametres.path + "yolov4-tiny-custom_final.weights",
                        Parametres.path + "yolov4-tiny-custom-2.cfg") #Defining network
classes = []
with open (Parametres.path + "obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Définition des couches de sortie 
layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Charger la vidéo
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600) #MLV_ dimension de limage 

waitToSendMsg = False
knifeDetect_time = 0

while True:
    _, img = cap.read()
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 0.00392, (320, 320), (0,0,0), swapRB=True, crop=False)
    
    start_time = time.time()
    knifeDetected = False

    net.setInput(blob)
    outs = net.forward(outputlayers)

    # Afficher les information sur l'écran et detection des objets
    class_ids=[]
    confidences=[]
    boxes=[]
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.1:
                # Objet détecté
                center_x= int(detection[0]*width)
                center_y= int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                # Coordonnées du rectangle
                x=int(center_x - w/2)
                y=int(center_y - h/2)

                boxes.append([x,y,w,h]) # Mettre tous les rectangles
                confidences.append(float(confidence)) # Mettre les confidence de detection des objects
                class_ids.append(class_id) # Mettre le nom de l'objet detecté

    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
            classeDetect = str(classes[class_ids[i]])
            label = classeDetect + '  ' + str(round(confidences[i],2))
            if classeDetect == "Person":
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2) # Boite verte autour des personnes
                liste = TransformeIntEnMSBLSB(x+w,x,y+h,y)
                print(liste)
                EnvoyerCoord(0xA7,liste)
                #EnvoyerCoord(0xA7, liste)
                print(  "Classe : " + classeDetect + 
                    ", Confidence : " + str(round(confidences[i],2)) +
                    ", x min : " + str(x) + ", y min : " + str(y) +
                    ", x max : " + str(x+w) + ", y max : " + str(y+h))
            else :
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) # Boite rouge autour des couteaux
                knifeDetected = True
                
            cv2.putText(img,label,(x,y+30),font,1,(255,255,255),2) # Afficher la classe et la confidence des objets détectés
            

    cv2.imshow("Image",img)
    # Show FPS
    fps = 1.0 / (time.time() - start_time)
    print("FPS: %.2f" % fps)

    # Envoie de message
    if knifeDetected and not waitToSendMsg:
        end_time = (time.time() - knifeDetect_time)

        # Temps au moment ou le couteau est detecté
        knifeDetect_time = time.time()
        # Sauvegarder l'image avec le couteau
        cv2.imwrite(Parametres.path + 'knife_pos.png', img)
        try:
            # Créer un objet de classe Envoi_Courriel
            courriel = Envoi_Courriel(Parametres.server, Parametres.port, Parametres.sender, Parametres.password, True)
            # Envoyer un simple courriel text
            #courriel.Send_Txt_Msg(Parametres.to_sms, Parametres.sender, Parametres.subject, Parametres.msg_sms)
            # Envoyer un courriel text avec pièce jointe
            # courriel.Send_Txt_Msg_Attachment(Parametres.to, Parametres.sender, Parametres.subject, Parametres.msg, Parametres.attachment)
        except (smtplib.SMTPException) as error:
            print("Problème dans l'utilisation de la classe Envoi_Courriel")
            print('Raison:\n', error)
        waitToSendMsg = True

    # Attendre 2 min entre chaque envoie de couriel
    elif (time.time() - knifeDetect_time) > 60:  
        waitToSendMsg = False
    
    # Pause de 100 ms
    time.sleep(0.1)

    key = cv2.waitKey(1)
    if key == 27:
        break
    if key == ord('m'):
        print("MANUELLE ***************************************ON")
        EnvoyerCoord(0xA1)
    if key == ord('o'):
        print("MANUELLE ***************************************OFF")
        EnvoyerCoord(0xA0)  

cap.release()
cv2.destroyAllWindows()