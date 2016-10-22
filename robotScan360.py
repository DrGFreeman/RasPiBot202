import matplotlib.pyplot as plt
import numpy as np
import time
import robotBuilder

def scan360(nbPts):
    turnSpeed = .18
    timeOneRev = 7.1
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
    scanX, scanY = scan360(180)

    plt.scatter(0, 0, c = 'r', s = 20)
    plt.scatter(scanX, scanY)
    plt.gca().set_aspect('equal')
    plt.show()

except KeyboardInterrupt:
    rpb202.stop()

