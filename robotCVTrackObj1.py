print "Importing libraries"
import time
import PID
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


##  PID controler gains
    Kp = .22 #.20 # Proportional term gain
    Ki = .04 #.04 # Integral term gain
    Kd = .008 #.007 # Derivative term gain

    pid = PID.PID(Kp, Ki, Kd)
    pid.setMedianFilter(False)

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

##          Calculate turn correction factor - PID controler
            turnCorr = -pid.getOutput(0, objTracker.getObjHPos(), tStep)
##            print turnCorr

##          Stop if object is close (based on area)
            if objTracker.getObjAreaRatio() > .28:
                fwd = 0

##         Reduce turn correction and speed if object is far
            if objTracker.getObjAreaRatio() < .002:
                turnCorr = .1 * turnCorr

##         Reduce speed if error is large

            speedCorr = 1 - .6 * abs(pid.getError())
                
        else:
            
##          Otherwise reset PID
            pid.reset()
            fwd = 0
            
##          Turn in last turn direction
            if lastTurn < 0:
                turn = -.13
            else:
                turn = .13

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
