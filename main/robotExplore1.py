import numpy as np
import time
import robotBuilder

def scanTurnToMax():

    turnSpeed = .4
    timeOneRev = 2.86 # 2.3
    nbPts = 45
    tStep = timeOneRev / nbPts
    data = np.array([[],[]])
    dist = []
    t = []
    for step in range(nbPts):
        time.sleep(.15)
        rpb202.readAStar()
        dist.append(snrCtr.getObstDist())
        t.append(step * tStep)
        rpb202.turn(turnSpeed)
        time.sleep(tStep)
        rpb202.stop()

    indexMax = np.argmax(dist)
    tIndexMax = t[indexMax]
    distMax = dist[indexMax]
    print "Scan completed, distance max ", distMax, " at index ", indexMax
    
    rpb202.turn(-turnSpeed)
    time.sleep(.90 * (t[-1] - tIndexMax))
    rpb202.stop()

    return distMax

def scanTurnToMax270():

    turnSpeed = .4
    timeScan= 1.6 # 2.3
    nbPts = 36
    tStep = timeScan / nbPts
    data = np.array([[],[]])
    dist = []
    t = []

    rpb202.turn(-turnSpeed)
    time.sleep(.7)
    rpb202.stop()
    
    for step in range(nbPts):
        time.sleep(.15)
        rpb202.readAStar()
        dist.append(snrCtr.getObstDist())
        t.append(step * tStep)
        rpb202.turn(turnSpeed)
        time.sleep(tStep)
        rpb202.stop()

    indexMax = np.argmax(dist)
    tIndexMax = t[indexMax]
    distMax = dist[indexMax]
    print "Scan completed, distance max ", distMax, " at index ", indexMax
    
    rpb202.turn(-turnSpeed)
    time.sleep(.90 * (t[-1] - tIndexMax))
    rpb202.stop()

    return distMax

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

##  Create direct pointers to robot sensors
irDL = rpb202.sensors[0]
irAL = rpb202.sensors[1]
snrCtr = rpb202.sensors[2]
irAR = rpb202.sensors[3]
irDR = rpb202.sensors[4]

fps = 15.
tStep = 1 / fps

fwdSpeed = .3
turnSpeed = .4
turn = 0.

turnCorrRange = 400.
turnCorrGain = .15
speedCorrRange = 300.
speedCorrGain = 1.


try:

    end = False
    while not end:

    ##  Perform scan
        distMax = scanTurnToMax270()
        if distMax > 1500:
            distMax = 1500
        time.sleep(.3)

        tScan = time.time()

        move = True

        # Read aStar (sensors, buttons, etc.)
        rpb202.readAStar()

        # Set turn correction and speed correction off
        turnCorr = 0
        speedCorr = 1

        # Read sensors
        dL = irDL.hasObst()
        dR = irDR.hasObst()

        if dL and not dR:
            rpb202.turn(turnSpeed)
            time.sleep(tStep)
            rpb202.stop()
        elif dR and not dL:
            rpb202.turn(-turnSpeed)
            time.sleep(tStep)
            rpb202.stop()
        elif dR and dL:
            move = False
        
        while move:

            tMove = time.time()
            
            # Read aStar (sensors, buttons, etc.)
            rpb202.readAStar()

            # Set turn correction and speed correction off
            turnCorr = 0
            speedCorr = 1

            # Read sensors
            dL = irDL.hasObst()
            dR = irDR.hasObst()

            if irAL.hasObst(0, 600):
                aL = irAL.getObstDist()
                if aL < turnCorrRange:
                    turnCorr += -turnCorrGain * (turnCorrRange - aL) / turnCorrRange
                if aL < speedCorrRange:
                    speedCorr -= speedCorrGain * (speedCorrRange - aL) / speedCorrRange

            if irAR.hasObst(0, 600):
                aR = irAR.getObstDist()
                if aR < turnCorrRange:
                    turnCorr += turnCorrGain * (turnCorrRange - aR) / turnCorrRange
                if aR < speedCorrRange:
                    speedCorr -= speedCorrGain * (speedCorrRange - aR) / speedCorrRange

            if dL and not dR:
                print "Digital left"
                speedCorr = 0
                turnCorr -= .5 * turnCorrGain
            elif dR and not dL:
                print "Digital right"
                speedCorr = 0
                turnCorr += .5 * turnCorrGain
            elif dL and dR:
                print "Digital left & right"
                speedCorr = 0
                move = False

            fwd = fwdSpeed * speedCorr
            turn = turnCorr
            
            dist = snrCtr.getObstDist()
            if dist > .2 * distMax and dist > 300:
                if time.time() - tScan <= 8:
                    rpb202.move(fwd, turn)
                else:
                    print "Max move time reached"
                    move = False
            else:
                print "Min distance reached", distMax, dist
                move = False

            dt = time.time() - tMove
            if dt < tStep:
                time.sleep(tStep - dt)
            
        rpb202.stop()


except KeyboardInterrupt:
    rpb202.stop()

