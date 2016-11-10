import time
import robotBuilder
from WiiRemote import WiiRemote

##  Build Robot from robotBuilder (edit robotBuilder to customize robot)
rpb202 = robotBuilder.build()

try:
    
    wii = WiiRemote(1)
    wii.robotRemote(20)
    time.sleep(.5)

    fwd = 0
    turn = 0

    tStep = .05

    step = 0

    end = False
    while not end:

        t0 = time.time()

        rpb202.odometer.update()
        
        if step % 10 == 0:
            print rpb202.odometer.getPosXYPhi(), rpb202.odometer.getSpeed(), rpb202.odometer.getOmega()
        
        fwd = wii.stickV
        turn = -wii.stickH

        if -.05 < fwd and fwd < .05:
            fwd = 0
        if -.05 < turn and turn < .05:
            turn = 0

        if wii.btnA:
            end = True

        if wii.btnZ:
            rpb202.odometer.resetEncoders()

        if fwd < 0:
            turn = -turn

        rpb202.move(fwd, turn)

        dt = time.time() - t0
        if dt < tStep:
            time.sleep(tStep - dt)
        
    rpb202.stop()
    wii.release()
    

except KeyboardInterrupt:
    rpb202.stop()
    wii.release()
    print("KeyboardInterrupt")    
