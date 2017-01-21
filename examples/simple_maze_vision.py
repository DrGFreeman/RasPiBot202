# -*- coding: utf-8 -*-

##=============================================================================
##  Simple line maze solver using computer vision.
##=============================================================================
##
##  Maze is made of 1" wide green masking tape.
##  Works with simple maze without loops.
##  Starting point can be any dead-end in the maze.
##  End point is a green rectangle approx 8" x 8".
##
##  The robot starts by exploring the maze using left hand rule
##  Once the end point is found, the robot returns to its starting point
##  by the shortest path.
##
##=============================================================================
  
##  Import libraries
import sys
sys.path.append('../')
import math
from time import sleep
import SimpleCV
import robotbuilder
from camera import Camera


##=====================================
##  Functions

def analyseImage(img):
    """ This function emulates a 5 wide array of IR reflectance sensors
    by spliting the bottom band of the camera image in five square boxes
    and finding blobs corresponding to the line color en each image. The
    function takes a 128 x 96 pixels Simple CV image objet and returns a
    list of five values which can be either 1 if there is a line in the
    image or 0 if there is no line"""
    
    ##  Crop to keep only lower 25% band of image
    img = img.crop((0,72), (128, 96))

    ##  Isolate green color
    img = img.hueDistance(color=(55, 159, 101), minsaturation=50)
    img = img.binarize(110)
    
    ##  Split image in five
    images = []
    images.append(img.crop((0,0), (25,24)))
    images.append(img.crop((25,24), (50,0)))
    images.append(img.crop((50,0), (78,24)))
    images.append(img.crop((78,24), (103,0)))
    images.append(img.crop((103,0), (128,24)))

    ##  Detect blobs in each image and append 0 or 1 to 
    result = []
    for image in images:
        ##  Find blobs with a min size of 20 pixels
        blob = image.findBlobs(minsize=20)
        if blob is not None:
            result.append(1)
        else:
            result.append(0)

    return result

def followLineToIntersection():
    """ Function uses camera to follow line until an intersection is reached.
    It returns two lists from analyseImage() corresponding to the images taken
    when the intersection is first detected and when the robot has moved to the
    center of the intersection."""

    ##  Get initial image from camera and analyse it
    img = cam.getSimpleCVImage()
    res = analyseImage(img)

    ##  Follow line until an intersection or dead-end is found
    while res[0] == 0 and res[4] == 0 and res.count(1) != 0 :

        ##  Set turn rate
        if res[1] == 1 and res[2] == 0 and res[3] == 0:
            omega = omegaHigh
        elif res[1] == 1 and res[2] == 1 and res[3] == 0:
            omega = omegaLow
        elif res[1] == 0 and res[2] == 1 and res[3] == 0:
            omega = 0
        elif res[1] == 0 and res[2] == 1 and res[3] == 1:
            omega = -omegaLow
        elif res[1] == 0 and res[2] == 0 and res[3] == 1:
            omega = -omegaHigh

        ##  Set robot speed
        rpb202.motionCtrl.setSpeed(speed, omega)

        ## Get a new image from camera and analyse it
        img = cam.getSimpleCVImage()
        res = analyseImage(img)

    ##  Once intersection is found, move forward slightly to ensure proper
    ##  detection on both outer images of image array
    omega = 0
    rpb202.motionCtrl.setSpeed(speed, omega)
    sleep(0.03)
    ##  Get first intersection image and analyse it
    ##  This image determines if there are paths to the left and/or right
    img = cam.getSimpleCVImage()
    int1 = analyseImage(img)

    ##  Move to center of intersection
    rpb202.motionCtrl.forwardDist(speed, 103, stop=True, decel=True)

    ##  Get second intersection image and analyse it
    ##  This image determines if there is a path forward
    img = cam.getSimpleCVImage()
    int2 = analyseImage(img)

    ##  Print intersection configuration
    print int1
    print int2

    return int1, int2

##=====================================
## Main program setup

##  Create Robot object instance
rpb202 = robotbuilder.build()

##  Position camera to follow line
rpb202.panTilt.down()

##  Create camera object instance
cam = Camera(size=2)

##  Read camera white balance settings from disk
##  Use Camera.doWhiteBalance() method prior running this program
##  to create white balance settings file
cam.readWhiteBalance()

##  Define turn rates (low/high) for line following (in rad/s)
omegaLow = .35
omegaHigh = 1.

##  Define forward speed for line following (in mm/s)
speed = 240.

##  Define turn rate for maze turns (in rad/s)
omegaTurn = math.pi

##  Initialize empty list of turns
turns = []

##=====================================
##  Main program start

try:

    ##=====================================
    ##  Part 1 - Explore maze

    finished = False
    while not finished:

        ##  Follow line until intersection is reached
        int1, int2 = followLineToIntersection()

        ##  Take turn decision
        
        ##  Check if at the end point
        if int2.count(1) == 5:
            finished = True
            ##  Play a sound
            rpb202.aStar.play_notes("L16 V9 ceg>c")

        ##  Else if there is a possible left turn, turn left
        elif int1[0] == 1:
            print "Left turn"
            rpb202.motionCtrl.turnAngle(math.pi/2, omegaTurn)
            ##  Append turn to list if there were other possible paths
            if int1[4] == 1 or int2[1:4].count(1) >= 1:
                turns.append('L')

        ##  Else if there is a possible straight, go straight
        elif int1[1:4].count(1) >= 1:
            print "Straight"
            turns.append('S')

        ##  Else if there is a possible right turn, turn right
        elif int1[4] == 1:
            print "Right turn"
            rpb202.motionCtrl.turnAngle(-math.pi/2, omegaTurn)
            if int1[0] == 1 or int2[1:4].count(1) >= 1:
                turns.append('R')

        ##  Finally, it must be a dead-end so turn around!
        else:
            rpb202.motionCtrl.turnAngle(math.pi, omegaTurn)
            turns.append('U')

        print turns

    ##  Exploration complete, stop robot
    rpb202.stop()


    ##=====================================
    ##  Part 2 - Return to starting point

    ##  Eliminate dead-ends
    
    ##  While tere are 'U's in turns list
    while turns.count('U') > 0:
        ##  Find first 'U' in turns list
        index = turns.index('U')
        ##  Extract 'U' turn and turns before and after 'U'
        trio = []
        for i in range(3):
            trio.append(turns.pop(index - 1))
        ##  Define replacement turn
        if trio == ['L', 'U', 'L']:
            turn = 'S'
        elif trio == ['S', 'U', 'L']:
            turn = 'R'
        elif trio == ['L', 'U', 'S']:
            turn = 'R'
        elif trio == ['R', 'U', 'L']:
            turn = 'U'
        elif trio == ['S', 'U', 'S']:
            turn = 'U'
        ##  Insert replacement turn into turns list
        turns.insert(index - 1, turn)

    print "Shortest path:", turns

    ##  Inverse path
    turns.reverse()
    ##  Inverse left and right turns
    for i in range(len(turns)):
        turn = turns[i]
        if turn == 'R':
            turns[i] = 'L'
        elif turn == 'L':
            turns[i] = 'R'

    print "Inverse shortest path:", turns

    ##  Wait a few seconds before restarting
    sleep(2.5)
    rpb202.motionCtrl.turnAngle(math.pi, omegaTurn)

    ##  Follow inverse shortest path to starting point

    finished = False
    while not finished:

        ##  Follow line until intersection is reached
        int1, int2 = followLineToIntersection()

        ##  Take turn decision

        ##  Case of a left turn (no other option), turn left
        if int1[0] == 1 and int1[4] == 0 and int2[1:4].count(1) == 0:
            rpb202.motionCtrl.turnAngle(math.pi/2, omegaTurn)

        ##  Case of a right turn (no other option), turn right
        elif int1[4] == 1 and int1[0] == 0 and int2[1:4].count(1) == 0:
            rpb202.motionCtrl.turnAngle(-math.pi/2, omegaTurn)

        ##  Otherwise if turns list not empty, turn according to turns list
        elif len(turns) > 0:
            turn = turns.pop(0)
            if turn == 'L':
                rpb202.motionCtrl.turnAngle(math.pi/2, omegaTurn)
            elif turn == 'R':
                rpb202.motionCtrl.turnAngle(-math.pi/2, omegaTurn)

        ##  Otherwise the robot is at the starting point
        else:
            finished = True

    ##  U-Turn
    rpb202.motionCtrl.turnAngle(math.pi, omegaTurn)

    ##  Play a sound
    rpb202.aStar.play_notes("L16 V9 >cgec")
    sleep(.5)


##=====================================
##  End of the main program
    
##  User interrupt (Ctrl-C)   
except KeyboardInterrupt:
    print "Keyboard Interrupt"
    rpb202.stop()
    rpb202.kill()
    cam.close()

##  Stop and clean-up running threads
finally:
    rpb202.stop()
    rpb202.kill()
    cam.close()
