# -*- coding: utf-8 -*-
import SimpleCV
import time

def analyseImage(i):

    # Decoupage de la bordure inferieure
    i = i.crop((0,72), (128, 96))

    # Isolation du vert
    i = i.hueDistance(color=(75, 133, 103), minsaturation=50)
    i = i.binarize(70)
    

    # Découpage de l'image en cinq
    images = []
    i1 = i.crop((0,0), (25,24))
    images.append(i1)
    i2 = i.crop((25,24), (50,0))
    images.append(i2)
    i3 = i.crop((50,0), (78,24))
    images.append(i3)
    i4 = i.crop((78,24), (103,0))
    images.append(i4)
    i5 = i.crop((103,0), (128,24))
    images.append(i5)

    # Détection des lignes dans chaque image
    blob01 = []
    for item in images:
        blob = item.findBlobs(minsize=20)
        if blob is not None:
            blob01.append(1)
        else:
            blob01.append(0)

    return blob01
