import time
import robotBuilder
from WiiRemote import WiiRemote

##  Build Robot from robotBuilder (edit robotBuilder to customize robot)
rpb202 = robotBuilder.build()
s0 = rpb202.sensors[0]
s1 = rpb202.sensors[1]
s2 = rpb202.sensors[2]
s3 = rpb202.sensors[3]
s4 = rpb202.sensors[4]

try:

# WiiRemote - Constantes
    
    wii = WiiRemote(1)
    wii.robotRemote(20)
    time.sleep(.5)

    fwd = 0
    turn = 0

    tStep = .05

    end = False
    while not end:

        t0 = time.time()

        
        
        fwd = wii.stickV
        turn = -wii.stickH

        if -.05 < fwd and fwd < .05:
            fwd = 0
        if -.05 < turn and turn < .05:
            turn = 0

        if wii.btnA:
            end = True

        

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
