print "Importing libraries"
import time
import robotBuilder

##  Build Robot from robotBuilder (edit robotBuilder to customize robot)
print "Configuring robot"
rpb202 = robotBuilder.build(True)

##  Create direct pointer to camera object tracker
print "Connecting camera"
objTracker = rpb202.camera.objTracker
objTracker.setDisplay(False)


try:

    print "Starting main program"
##  Initialization of turn and speed variables
    turn = 0  # Turn speed
    turnCorr = 0  # Turn speed correction factor
    lastTurn = 0  # Last turn speed

    fwd = 0  # Forward speed
    speedCorr = 1  # Forward speed correction factor

##  Error terms for PID controller
    err = 0  # Horizontal position error (target rel to camera center)
    errInt = 0  # Integral of position error
    errDer = 0  # Derivative of position error
    errPrev = 0  # Previous error (for derivative calculation)

##  PID controler gains
    Kp = .18 #.20 # Proportional term gain
    Ki = .06 #.04 # Integral term gain
    Kd = .012 #.007 # Derivative term gain
    KpMod = 1  # Proportional gain modifier used when target is far away used to avoid losing target

##  Main loop time step
    fps = 20.
    tStep = 1 / fps

##  Launch object tracker
    objTracker.trackObjByHue(74, fps)

##  Main loop
    end = False
    while not end:

        t0 = time.time()

##      Check if object in sight
        if objTracker.hasObj():

##          Calculate error terms
            err = objTracker.getObjHPos()
            errInt += err * tStep
            errDer = (err - errPrev) / tStep
            errPrev = err
##          Stop if object is close (based on area)
            if objTracker.getObjAreaRatio() > .28:
                fwd = 0
##          Apply proportional gain correction if object is far
            if objTracker.getObjAreaRatio() < .002:
                KpMod = .1
            else:
                KpMod = 1
##      Otherwise reset error terms to zero
        else:
            err = 0
            errInt = 0
            errDer = 0
            errPrev = 0
            fwd = 0
##          Turn in last turn direction
            if lastTurn < 0:
                turn = -.13
            else:
                turn = .13

##      Calculate turn correction factor - PID controler
        turnCorr = Kp * KpMod * err + Ki * errInt + Kd * errDer

##      Apply speed and turn correction factors
        fwd = fwd * speedCorr
        turn = turn + turnCorr

##      Move robot
        rpb202.move(fwd, turn)

##      Reset turn and speed variables
        lastTurn = turn
        turn = 0
        turnCorr = 0
        fwd = .3
        speedCorr = 1

##      Calculate and apply delay to reach time step
        dt = time.time() - t0
        if dt < tStep:
            time.sleep(tStep - dt)

##  End of main loop. Stop robot and threads
    rpb202.stop()
    rpb202.camera.stop()
    objTracker.stop()
        
##  Use Ctrl-C to end
except KeyboardInterrupt:
    rpb202.stop()
    rpb202.camera.stop()
    objTracker.stop()
    print "\nExiting program"
    time.sleep(1)
