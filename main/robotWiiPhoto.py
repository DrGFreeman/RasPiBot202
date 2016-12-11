import time
import robotBuilder
from WiiRemote import WiiRemote

##  Build Robot from robotBuilder (edit robotBuilder to customize robot)
rpb202 = robotBuilder.build(True)

cam = rpb202.camera.camera

prefix = raw_input("Enter image file prefix: ")
index = int(raw_input("Enter starting index: "))

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

        img = cam.getImage()        
        img.show()
        
        fwd = wii.stickV
        turn = -wii.stickH

        if -.05 < fwd and fwd < .05:
            fwd = 0
        if -.05 < turn and turn < .05:
            turn = 0

        if wii.btnA:
            end = True

        if wii.btnZ:
            name = prefix + str(index) + ".png"
            img.save(name)
            print "Image saved as " + name
            index += 1

        if fwd < 0:
            turn = -turn

        rpb202.move(fwd, turn)

        dt = time.time() - t0
        if dt < tStep:
            time.sleep(tStep - dt)
        
    rpb202.stop()
    wii.release()
    rpb202.camera.stop()

except KeyboardInterrupt:
    rpb202.stop()
    wii.release()
    print("KeyboardInterrupt")    
