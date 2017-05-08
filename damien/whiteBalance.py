import sys
sys.path.append('../')
import time
from camera import Camera

cam = Camera()

print "Place a white sheet in front of camera"
for r in range(5, 0, -1):
    print "Calibration will start in " + str(r) + " seconds"
    time.sleep(1)
    
cam.doWitheBalance()

cam.close()
