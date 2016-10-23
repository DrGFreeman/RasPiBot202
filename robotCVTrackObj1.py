import time
import robotBuilder
from WiiRemote import WiiRemote

##  Build Robot from robotBuilder (edit robotBuilder to customize robot)
rpb202 = robotBuilder.build(True)

##  Create direct pointer to camera object tracker
objTracker = rpb202.camera.objTracker

try:

    tStep = .1

    end = False
    while not end:

        t0 = time.time()

        objTracker.trackObjByHue(80)

        if objTracker.hasObj():
            print objTracker.getObjHPos()

        dt = time.time() - t0
        if dt < tStep:
            time.sleep(tStep - dt)

    rpb202.stop()
    rpb202.camera.stop()
    rpb202.objTracker.stop()
        

except KeyboardInterrupt:
    rpb202.stop()
    rpb202.camera.stop()
    rpb202.objTracker.stop()
    print "KeyboardInterrupt"
