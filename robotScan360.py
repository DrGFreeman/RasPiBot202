import matplotlib.pyplot as plt
import numpy as np
import time
import robotBuilder

def scanTurnToMax():

    turnSpeed = .4
    timeOneRev = 2.3
    nbPts = 30
    tStep = timeOneRev / nbPts
    data = np.array([[],[]])
    dist = []
    t = []
    for step in range(nbPts + 2):
        time.sleep(.3)
        rpb202.readAStar()
        dist.append(snrCtr.getObstDist())
        t.append(step * tStep)
        rpb202.turn(turnSpeed)
        time.sleep(tStep)
        rpb202.stop()

    indexMax = np.argmax(dist)
    print dist[indexMax]
    tIndexMax = t[indexMax]
    print indexMax

    rpb202.turn(-turnSpeed)
    time.sleep(t[-1] - tIndexMax)
    rpb202.stop()

    return t, dist

def scan360(nbPts):
    turnSpeed = .25
    timeOneRev = 4.5
    thetaStep = 2 * np.pi / nbPts
    theta = np.pi / 2
    thetaPts = []
    distPts = []
    xPts = []
    yPts = []
    dist = 0
    for step in range(nbPts):
        
        rpb202.readAStar()
        dist = snrCtr.getObstDist()

        thetaPts.append(theta)
        distPts.append(dist)
        xPts.append(dist * np.cos(theta))
        yPts.append(dist * np.sin(theta))
        
        rpb202.turn(turnSpeed)
        time.sleep(timeOneRev / nbPts)

        theta += thetaStep

    rpb202.stop()    
    return xPts, yPts
    
##  Build robot
rpb202 = robotBuilder.build()
##  Create pointer to sonar sensor
snrCtr = rpb202.sensors[2]

try:
    ##  Perform scan

    scanT, scanD = scanTurnToMax()

##    plt.scatter(0, 0, c = 'r', s = 20)
##    plt.scatter(scanT, scanD)
##    #plt.gca().set_aspect('equal')
##    plt.show()

except KeyboardInterrupt:
    rpb202.stop()

