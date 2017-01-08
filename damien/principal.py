# -*- coding: utf-8 -*-

# Importation des modules externes
import sys
sys.path.append("../")
from robotbuilder import build
from analyseImage import analyseImage
from camera import Camera
from time import sleep
import math

# Creation du robot
r2 = build()

# Positionnement de la camera
r2.panTilt.down()

# Creation des variables
cam = Camera(size = 2)  # Objet Camera
vitesse = 200.          # Vitesse de déplacement en mm/s
vRot1 = 1.              # Vitesse de rotation rapide en radians/s
vRot2 = .25             # Vitesse de rotation lente en radians/s
vVirage = 2.            # Vitesse de virage en radians/s
compt = 0               # Compteur pour noms de fichiers photos
fin = False             # Pour savoir si une boucle est terminée


# Reglage de la camera
cam.picam.awb_mode = 'sunlight'

# Programme principal
try:
    
    # Exploration du labyrinthe

    # Creation de la liste des virages
    listeV = []

    while not fin:

        # Prise de la photo
        img = cam.getSimpleCVImage()
        res = analyseImage(img)


        # Suivi de la ligne
        # Tant que pas intersection ou cul de sac
        while res[0] == 0 and res[4] == 0 and res.count(1) != 0 :

            # Determination vitesse Rotation
            if res[1] == 1 and res[2] == 0 and res[3] == 0:
                vRot = vRot1
            elif res[1] == 1 and res[2] == 1 and res[3] == 0:
                vRot = vRot2
            elif res[1] == 0 and res[2] == 1 and res[3] == 0:
                vRot = 0
            elif res[1] == 0 and res[2] == 1 and res[3] == 1:
                vRot = -vRot2
            elif res[1] == 0 and res[2] == 0 and res[3] == 1:
                vRot = -vRot1

            # Deplacement du robot
            r2.motionCtrl.move(vitesse, vRot)

            # Prise de la photo
            img = cam.getSimpleCVImage()
            res = analyseImage(img)


        # Avance un peu pour detecter l'intersection
        vRot = 0
        r2.motionCtrl.move(vitesse, vRot)
        sleep(0.03)
        img = cam.getSimpleCVImage()
        res = analyseImage(img)

        # Sauvegarde des images d'intersection
        nom = './images/int' + str(compt) + '.png'
        img.save(nom)
        compt += 1

        # Avance au centre de l'intersection
        r2.motionCtrl.forwardDist(vitesse, 110, stop=True, decel=True)

        # Prend une image pour savoir si l'intersection continue
        # ou si c'est la fin
        img = cam.getSimpleCVImage()
        resInt = analyseImage(img)
        
        print res
        print resInt


        # Decision du virage
        # Detection de l'arrivee
        if resInt.count(1) == 5:
            fin = True
        # Detection d'une ligne a gauche
        elif res[0] == 1:
            #tourne a gauche
            print ("Gauche")
            r2.motionCtrl.turnAngle(math.radians(90), vVirage)
            if res[4] == 1 or resInt[1:4].count(1) >= 1:
                listeV.append('G,)
        # Detection d'une ligne en avant
        elif resInt[1:4].count(1) >= 1:
            #continue tout droit
            print("Tout droit")
            listeV.append('L')
        # Detection d'une ligne a droite
        elif res[4] == 1:
            #tourne a droite
            print("Droite")
            r2.motionCtrl.turnAngle(-math.radians(90), vVirage)
            if res[0] == 1 or resInt[1:4].count(1) >= 1:
                listeV.append('D')
        # Sinon c'est un cul-de-sac
        else:
            # Demi tour
            print("Demi tour")
            r2.motionCtrl.turnAngle(math.radians(180), vVirage)
            listeV.append('U')

        sleep(.1)
        print(listeV)

    # Arret du robot
    r2.stop()
        
    # Elimination des culs-de-sac
    # Tant qu'il y a des U
    while listeV.count('U') > 0:
        # Position du premier U
        iu = listeV.index('U')
        # Extraction du U et des deux virages autour du U
        vir = []
        for i in range(3):
            vir.append(listeV.pop(iu -1))
        # Determination du virage de remplacement
        if vir == ['G', 'U', 'G']:
            vir = 'L'
        elif vir == ['L', 'U', 'G']:
            vir = 'D'
        elif vir == ['G', 'U', 'D']:
            vir = 'U'
        elif vir == ['G', 'U', 'L']:
            vir = 'D'
        elif vir == ['D', 'U', 'G']:
            vir = 'U'
        elif vir == ['L', 'U', 'L']:
        # Insertion du virage de remplacement
        listeV.insert(iu - 1, vir)

    print("Parcours optimal: " + str(listeV))

    # Inversion des virages
    for i in range(len(listeV)):
	vir = listeV[i]
	if vir == 'D':
		listeV[i] = 'G'
	elif vir == 'G':
		listeV[i] = 'D'

    # Inversion du parcours
    listeV.reverse()

    print("Parcours inverse: " + str(listeV))

    sleep(3)

    # Parcours a l'envers
    r2.motionCtrl.turnAngle(math.radians(180), vVirage)
    
    fin = False
    while not fin:

        # Prise de la photo
        img = cam.getSimpleCVImage()
        res = analyseImage(img)


        # Suivi de la ligne
        # Tant que pas intersection ou cul de sac
        while res[0] == 0 and res[4] == 0 and res.count(1) != 0 :

            # Determination vitesse Rotation
            if res[1] == 1 and res[2] == 0 and res[3] == 0:
                vRot = vRot1
            elif res[1] == 1 and res[2] == 1 and res[3] == 0:
                vRot = vRot2
            elif res[1] == 0 and res[2] == 1 and res[3] == 0:
                vRot = 0
            elif res[1] == 0 and res[2] == 1 and res[3] == 1:
                vRot = -vRot2
            elif res[1] == 0 and res[2] == 0 and res[3] == 1:
                vRot = -vRot1

            # Deplacement du robot
            r2.motionCtrl.move(vitesse, vRot)

            # Prise de la photo
            img = cam.getSimpleCVImage()
            res = analyseImage(img)


        # Avance un peu pour detecter l'intersection
        vRot = 0
        r2.motionCtrl.move(vitesse, vRot)
        sleep(0.03)
        img = cam.getSimpleCVImage()
        res = analyseImage(img)

        # Sauvegarde des images
        nom = './images/int' + str(compt) + '.png'
        img.save(nom)
        compt += 1

        # Avance au centre de l'intersection
        r2.motionCtrl.forwardDist(vitesse, 110, stop=True, decel=True)

        # Prend une image pour savoir si l'intersection continue ou si c'est la fin
        img = cam.getSimpleCVImage()
        #img.save("img2.png")
        resInt = analyseImage(img)
        print res
        print resInt

        if len(listeV) > 0:
            # Decision du virage
            # Cas d'un virage a gauche
            if res[0] == 1 and res[4] == 0 and resInt[1:4].count(1) == 0:
                    # Tourne a gauche
                    r2.motionCtrl.turnAngle(math.radians(90), vVirage)
            # Cas d'un virage a droite
            elif res[4] == 1 and res[0] == 0 and resInt[1:4].count(1) == 0:
                    # Tourne a droite
                    r2.motionCtrl.turnAngle(-math.radians(90), vVirage)
            # Sinon on tourne selon la liste de virages
            else:
                vir = listeV.pop(0)
                if vir == 'G':
                    r2.motionCtrl.turnAngle(math.radians(90), vVirage)
                elif vir == 'D':
                    r2.motionCtrl.turnAngle(-math.radians(90), vVirage)

            sleep(.1)
        else:
            fin = True
        
    # Demi tour
    r2.motionCtrl.turnAngle(math.radians(180), vVirage)
    
    # Arret du robot
    r2.stop()
    r2.kill()
    cam.close()
              

except KeyboardInterrupt:
    r2.stop()
    r2.kill()
    cam.close()
    print("Interruption du programme")
