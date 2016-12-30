import sys
sys.path.append("../")
import matplotlib.pyplot as plt
import robotbuilder
from timer import Timer


r = robotbuilder.build()

t = Timer() # Excecution timer
l = Timer() # Loop timer

left = []
right = []
timeData = []

time = 0

try:

    go = True
    while t.isWithin(7):

        if t.isWithin(6):
            r.motionCtrl.setSpeed(250, 0)
        elif t.isWithin(4):
            r.motionCtrl.move(325, 0)
        elif t.isWithin(6):
            r.motionCtrl.move(200, 0)
        else:
            r.motionCtrl.stop()
            
        l.sleepToElapsed(.05)

        left.append(r.odometer.speedL)
        right.append(r.odometer.speedR)
        timeData.append(time)

        time += .05

    plt.plot(timeData, left)
    plt.plot(timeData, right)
    plt.show()

except KeyboardInterrupt:
    r.motionCtrl.stop()
