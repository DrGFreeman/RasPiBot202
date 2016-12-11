import matplotlib.pyplot as plt
import robotBuilder
from Timer import Timer


r = robotBuilder.build()
m = r.motors

t = Timer()
l = Timer()

left = []
right = []
timeData = []

time = 0

try:

    go = True
    while t.isWithin(7):

        if t.isWithin(2.5):
            r.motionCtrl.setSpeed(250, 0)
        elif t.isWithin(5):
            r.motionCtrl.move(325, 0)
        elif t.isWithin(6):
            r.motionCtrl.move(200, 0)
        elif go:
            r.motionCtrl.stop()
            go = False
            
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
