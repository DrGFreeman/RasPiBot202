##  Simple example to demonstrate base functionality
##
##  The robot will execute a counter-clockwise cirle of a given diameter

##  Minimum libraries to import
import sys
sys.path.append('../')
import time
import robotbuilder

##  Optional libraries used in this example
from timer import Timer
from math import pi, degrees

##  Create Robot object instance
rpb202 = robotbuilder.build()

##  Set program loop time step
timeStep = .02

##  Set motion controller refresh time step
rpb202.motionCtrl.setTimeStep(timeStep)

##  Define program specific variables
diameter = 400  # Circle diameter in mm
speed = 125  # Forward speed in mm/s
moveTime = pi * diameter / speed  # Time to complete full circle

# Turn rate in radians/s (360deg = 2*pi radians), positive = ccw
omega = 2 * pi / moveTime

try:

    ##  Initialize loop timer
    loopTimer = Timer()

    phi = 0  # Robot angle relative to start position
    
    fullSpeed = True
    
    ##  Main loop
    while phi < 2 * pi - 1.1 * omega * timeStep:

        if fullSpeed and phi > 1.95 * pi:
            speed /= 2
            omega /= 2
            fullSpeed = False
        
        ##  Give speed and turn rate target
        ##  The arguments of this method are typically updated every pass
        ##  of the main loop. In this example they remain mostly consant.
        rpb202.motionCtrl.setSpeed(speed, omega)

        ##  Wait until end of time step
        loopTimer.sleepToElapsed(timeStep)
        
        phi = rpb202.odometer.getPhi()
        print round(degrees(phi), 1)
        
    print rpb202.odometer.getPosXY()

except KeyboardInterrupt:
    print "Keyboard Interrupt"
    rpb202.stop()
    rpb202.kill()

finally:
    rpb202.stop()
    rpb202.kill()
