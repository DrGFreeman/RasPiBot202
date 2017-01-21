# -*- coding: utf-8 -*-

# Importation des modules externes
import sys
sys.path.append("../")
from robotbuilder import build
from analyseImage import analyseImage
from camera import Camera
from time import sleep
import math

# Création du robot
rpb202 = build()

# Positionnement de la camera
rpb202.panTilt.down()

# Création des variables
cam = Camera(size = 2)  # Objet Camera
vitesse = 200.          # Vitesse de déplacement en mm/s
vRot1 = 1.              # Vitesse de rotation rapide en radians/s
vRot2 = .35             # Vitesse de rotation lente en radians/s
vVirage = 3.            # Vitesse de virage en radians/s
compt = 0               # Compteur pour noms de fichiers photos
fin = False             # Pour savoir si une boucle est terminée

# Réglage de la camera (balance des blancs)
cam.readWhiteBalance()

# Programme principal
try:

    #==========================
    # Exploration du labyrinthe

    # Création de la liste des virages
    listeV = []

    while not fin:

        # Prise de la photo
        img = cam.getSimpleCVImage()
        res = analyseImage(img)


        # Suivi de la ligne
        # Tant que pas intersection ou cul de sac
        while res[0] == 0 and res[4] == 0 and res.count(1) != 0 :

            # Détermination vitesse Rotation
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

            # Déplacement du robot
            rpb202.motionCtrl.move(vitesse, vRot)

            # Prise de la photo
            img = cam.getSimpleCVImage()
            res = analyseImage(img)

        # Avance un peu pour détecter l'intersection
        vRot = 0
        rpb202.motionCtrl.move(vitesse, vRot)
        sleep(0.03)
        img = cam.getSimpleCVImage()
        res = analyseImage(img)

        # Sauvegarde des images d'intersection
        nom = './images/int' + str(compt) + '.png'
        img.save(nom)
        compt += 1

        # Avance au centre de l'intersection
        rpb202.motionCtrl.forwardDist(vitesse, 105, stop=True, decel=True)

        # Prend une image pour savoir si l'intersection continue
        # ou si c'est la fin
        img = cam.getSimpleCVImage()
        resInt = analyseImage(img)

        # Affichage de la configuration d'intersection
        print res
        print resInt

        # Décision du virage
        # Détection de l'arrivee
        if resInt.count(1) == 5:
            fin = True
            # Jouer un son
            rpb202.aStar.play_notes("L16 V9 ceg>c")
        # Détection d'une ligne a gauche
        elif res[0] == 1:
            # Tourne a gauche
            print("Gauche")
            rpb202.motionCtrl.turnAngle(math.radians(90), vVirage)
            if res[4] == 1 or resInt[1:4].count(1) >= 1:
                listeV.append('G')
        # Détection d'une ligne en avant
        elif resInt[1:4].count(1) >= 1:
            # Continue tout droit
            print("Tout droit")
            listeV.append('L')
        # Détection d'une ligne a droite
        elif res[4] == 1:
            # Tourne a droite
            print("Droite")
            rpb202.motionCtrl.turnAngle(-math.radians(90), vVirage)
        # Sinon c'est un cul-de-sac
        else:
            # Demi-tour
            print("Demi tour")
            rpb202.motionCtrl.turnAngle(math.radians(180), vVirage)
            listeV.append('U')

        sleep(.1)
        print(listeV)

    # Arrêt du robot
    rpb202.stop()

    #============================
    # Élimination des culs-de-sac
    
    # Tant qu'il y a des U
    while listeV.count('U') > 0:
        # Position du premier U
        iu = listeV.index('U')
        # Extraction du U et des deux virages autour du U
        vir = []
        for i in range(3):
            vir.append(listeV.pop(iu -1))
        # Détermination du virage de remplacement
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
            vir = 'U'
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

    #sleep(3)
    raw_input("Appuyez sur 'Enter' pour continuer")

    #====================
    # Parcours a l'envers

    # Demi-tour
    rpb202.motionCtrl.turnAngle(math.radians(180), vVirage)
    
    fin = False
    while not fin:

        # Prise de la photo
        img = cam.getSimpleCVImage()
        res = analyseImage(img)


        # Suivi de la ligne
        # Tant que pas intersection ou cul de sac
        while res[0] == 0 and res[4] == 0 and res.count(1) != 0 :

            # Détermination vitesse Rotation
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

            # Déplacement du robot
            rpb202.motionCtrl.move(vitesse, vRot)

            # Prise de la photo
            img = cam.getSimpleCVImage()
            res = analyseImage(img)

        # Avance un peu pour detecter l'intersection
        vRot = 0
        rpb202.motionCtrl.move(vitesse, vRot)
        sleep(0.03)
        img = cam.getSimpleCVImage()
        res = analyseImage(img)

        # Sauvegarde des images
        nom = './images/int' + str(compt) + '.png'
        img.save(nom)
        compt += 1

        # Avance au centre de l'intersection
        rpb202.motionCtrl.forwardDist(vitesse, 105, stop=True, decel=True)

        # Prend une image pour savoir si l'intersection continue
        # ou si c'est la fin
        img = cam.getSimpleCVImage()
        resInt = analyseImage(img)

        # Affichage de la configuration d'intersection
        print res
        print resInt

        # Décision du virage
        # Cas d'un virage a gauche
        if res[0] == 1 and res[4] == 0 and resInt[1:4].count(1) == 0:
                # Tourne a gauche
                rpb202.motionCtrl.turnAngle(math.radians(90), vVirage)
        # Cas d'un virage a droite
        elif res[4] == 1 and res[0] == 0 and resInt[1:4].count(1) == 0:
                # Tourne a droite
                rpb202.motionCtrl.turnAngle(-math.radians(90), vVirage)
        # Sinon on tourne selon la liste de virages
        elif len(listeV) > 0:
            vir = listeV.pop(0)
            if vir == 'G':
                rpb202.motionCtrl.turnAngle(math.radians(90), vVirage)
            elif vir == 'D':
                rpb202.motionCtrl.turnAngle(-math.radians(90), vVirage)
        else:
            fin = True

        sleep(.1)
        
    # Demi-tour
    rpb202.motionCtrl.turnAngle(math.radians(180), vVirage)

    # Jouer un son
    rpb202.aStar.play_notes("L16 V9 >cgec")
    
#===========================
# Fin du programme principal

# Arrêt par l'utilisateur (Ctrl-C)
except KeyboardInterrupt:
    rpb202.stop()
    rpb202.kill()
    cam.close()
    print("Interruption du programme")

# Arrêt des processus en cours (robot et caméra)
finally:
    rpb202.stop()
    rpb202.kill()
    cam.close()
