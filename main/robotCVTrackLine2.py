print "Importing libraries"
import math
import robotBuilder
from PID import PID
from Timer import Timer

import time

from WiiRemote import WiiRemote

##  Build Robot from robotBuilder (edit robotBuilder to customize robot)
print "Configuring robot"
rpb202 = robotBuilder.build(True)

##  Create direct pointer to camera object tracker
print "Connecting camera"
lineTracker = rpb202.camera.lineTracker
lineTracker.setDisplay(False)


try:

    print "Starting main program"

    wii = WiiRemote(1)
    wii.robotRemote(20)
    time.sleep(.5)

##  Initialization of turn and speed variables
    targetSpeed = 450  # Forward speed target (straight line)


##  Main loop time step
    fps = 20.
    tStep = 1 / fps
    rpb202.motionCtrl.setTimeStep(tStep)
    

##  Launch object tracker
    lineTracker.trackLines(fps)
    loopTimer = Timer()

    Kp = .27
    Ki = .03
    Kd = .03

    pid = PID(Kp, Ki, Kd)

##  Main loop
    end = False
    while not end:

        if wii.btnA:
            print Kp, Ki, Kd, targetSpeed
            Kp = float(raw_input("Nouveau Kp: "))
            Ki = float(raw_input("Nouveau Ki: "))
            Kd = float(raw_input("Nouveau Kd: "))
            targetSpeed = int(raw_input("Nouveau targetSpeed: "))
            pid.setKs(Kp, Ki, Kd)

##      Check if object in sight
        if lineTracker.hasLines():

##          Check line position on camera
            lineHPos = lineTracker.getLinesHPos(0)

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

##  End of main loop. Stop robot and threads
    rpb202.stop()
    rpb202.camera.stop()
    lineTracker.stop()
        
##  Use Ctrl-C to end
except KeyboardInterrupt:
    rpb202.stop()
    rpb202.camera.stop()
    lineTracker.stop()
    wii.release()
    print "\nExiting program"
    time.sleep(1)
