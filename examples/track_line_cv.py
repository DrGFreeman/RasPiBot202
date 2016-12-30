print "Importing libraries"
import sys
sys.path.append("../")
import math
import time
import robotbuilder
from pid import PID
from timer import Timer


##  Build Robot from robotBuilder (edit robotBuilder to customize robot)
print "Configuring robot"
rpb202 = robotbuilder.build(True)

##  Create direct pointer to camera object tracker
print "Connecting camera"
lineTracker = rpb202.camera.lineTracker
lineTracker.setDisplay(False)

try:

    print "Starting main program"

##  Initialization of turn and speed variables
    targetSpeed = 400  # Forward speed target (straight line)


##  Main loop time step
    fps = 20
    tStep = 1. / fps
    rpb202.motionCtrl.setTimeStep(tStep)
    

##  Launch object tracker
    lineTracker.trackLines(fps)
    loopTimer = Timer()

##  Set PID controller gains

    Kp = .27
    Ki = .03
    Kd = .03

    pid = PID(Kp, Ki, Kd)

##  Main loop
    while True:

##      Check if object in sight
        if lineTracker.hasLines():

##          Check line position on camera
            lineHPos = lineTracker.getLinesHPos(0)

##          Set turn rate
            omega = -pid.getOutput(0, lineHPos, tStep)

##          Calculate speed correction factor (slow-down if large error)
            speed = targetSpeed * (1 - 0.85 * lineHPos**2)

##          Move robot to follow line
            rpb202.motionCtrl.move(speed, omega)

##      Otherwise stop
        else:

            rpb202.motionCtrl.stop()

##      Finish time step
        loopTimer.sleepToElapsed(tStep)

        
##  Use Ctrl-C to end
except KeyboardInterrupt:
    rpb202.stop()
    rpb202.camera.stop()
    lineTracker.stop()
    print "\nExiting program"
    time.sleep(1)
