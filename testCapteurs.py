from a_star import AStar
import time
import math
import numpy

##def irGauche(a):
##    if a > 40 and a < 200:
##        dist = 1.094E-2 * a**2 - 7.865 * a + 1699
##    elif a >= 200 and a < 415:
##        dist = 4.822E-3 * a**2 - 4.732 * a + 1327
##    elif a >= 415 and a < 900:
##        dist = -5.345E-7 * a**3 + 1.55E-3 * a**2 - 1.59 * a + 615
##    else:
##        dist = -1
##    return dist

aStar = AStar()

try:

    print "Mesure en cours ..."
    dist = []
    t0 = time.time()
    
    while time.time() - t0 <= 10:
        analog = aStar.read_analog()
        time.sleep(.02)
        dist.append(analog[2])
        avg = numpy.mean(dist)
        stdev = numpy.std(dist)

    print "Moyenne: ",  avg
    print "Ecart type: ", stdev
    print "Nb pts: ", len(dist)

    while True:
        analog = aStar.read_analog()
        print(irGauche(analog[2]))
        time.sleep(.5)

except KeyboardInterrupt:
    print("KeyboardInterrupt")
