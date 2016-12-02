import math
from math import pi
import time
import robotBuilder
from PID import PID
from Timer import Timer
from Maze import Maze

########################################################################
##  Robot Movement Functions

##  Turn robot to heading
def turnToHeading(heading):
    rpb202.motionCtrl.turnToAngle(headingToAngle(heading))

def uTurn(currentHeading):
    rpb202.motionCtrl.turnToAngle(headingToAngle(currentHeading) + pi)

def forward(speed, time):
    timer = Timer()
    loopTimer = Timer()
    while timer.isWithin(time):
        rpb202.motionCtrl.move(speed, 0)
        loopTimer.sleepToElapsed(timeStep)
        

##  Follow line to next intersection. Return intersection type:  
    # 1 = path to left
    # 2 = path forward
    # 4 = path to right
    # Combinations of 1-2-4 (1, 3, 5, 6, 7) 
    # 0 = dead-end
    # 8 = finish
    # Will never return 2 (straight != intersection)
def followLineToInt(speed):

    omegaPID.reset()
    loopTimer = Timer()

    ##  Follow line until intersection is found
    while lineTracker.getIntersection() == 2:

        ##  Get turn rate from PID controller
        omega = -omegaPID.getOutput(0, lineTracker.getBtmHPos(), timeStep)
        rpb202.motionCtrl.move(speed, omega)

        loopTimer.sleepToElapsed(timeStep)
    rpb202.motionCtrl.stop()

    ##  Move forward slightly to ensure proper intersection detection
    rpb202.motionCtrl.forwardDist(200, 40)
    intersection = lineTracker.getIntersection()

    ##  Move to center of intersection
    rpb202.motionCtrl.forwardDist(150, 220)
    rpb202.motionCtrl.stop()
    
    return intersection

########################################################################
##  Pseudo Odometry Functions

def phiToHeading(phi):
    angleTol = pi / 12
    if 2 * pi - angleTol < phi or phi < angleTol:
        return 'E'
    elif pi / 2 - angleTol < phi and phi < pi / 2 + angleTol:
        return 'N'
    elif pi - angleTol < phi and phi < pi + angleTol:
        return 'W'
    elif 3 * pi / 2 - angleTol < phi and phi < 3 * pi / 2 + angleTol:
        return 'S'
    else:
        print "Angle outside of tolerance"

def correctedPos(x0, y0, dx, dy, heading):
    if heading == 'E' or heading == 'W':
        return x0 + dx, y0, abs(dx)
    elif heading == 'N' or heading == 'S':
        return x0, y0 + dy, abs(dy)

########################################################################
##  Maze Functions

##  Define next unvisited path heading at current node (in exploration mode)
def nextUnvisitedHeading(currentNode, currentHeading, intersection):
    currentAngle = headingToAngle(currentHeading)
    headings = []
    if intersection & 1 == 1:
        if currentAngle == 3 * pi / 2:
            headings.append(angleToHeading(0))
        else:
            headings.append(angleToHeading(pi / 2 + currentAngle))
    if intersection & 2 == 2:
        headings.append(angleToHeading(currentAngle))
    if intersection & 4 == 4:
        if currentAngle == 0:
            headings.append(angleToHeading(3 * pi / 2))
        else:
            headings.append(angleToHeading(currentAngle - pi / 2))
    for heading in headings:
        if maze.headingIsUnvisited(currentNode, heading):
            nextUnvisitedHeading = heading
    print "Next heading:", nextUnvisitedHeading
    return nextUnvisitedHeading

##  Convert heading to angle
def headingToAngle(heading):
    headings = ['E', 'N', 'W', 'S']
    angles = [0., pi / 2, pi, 3 * pi / 2]
    return angles[headings.index(heading)]

##  Convert angle to heading
def angleToHeading(angle):
    headings = ['E', 'N', 'W', 'S']
    angles = [0., pi / 2, pi, 3 * pi / 2]
    return headings[angles.index(angle)]

##  Define heading after left turn
def leftTurn(heading):
    headings = ['E', 'N', 'W', 'S']
    index = headings.index(heading)
    if index == 3:
        return headings[0]
    else:
        return headings[index + 1]

##  Define heading after right turn
def rightTurn(heading):
    headings = ['E', 'N', 'W', 'S']
    index = headings.index(heading)
    if index == 0:
        return headings[3]
    else:
        return headings[index - 1]

##  Calculate number of paths out of a node from intersection type
def nbPathsOut(intersection):
    nbPathsOut = 0
    if intersection & 1 == 1:
        nbPathsOut += 1
    if intersection & 2 == 2:
        nbPathsOut += 1
    if intersection & 4 == 4:
        nbPathsOut += 1
    return nbPathsOut


########################################################################
##  Main program
########################################################################

########################################################################
##  Initialize variables

speed = 300
Kp = .2
Ki = .03
Kd = 0.
omegaPID = PID(Kp, Ki, Kd)

fps = 20.
timeStep = 1 / fps

rpb202 = robotBuilder.build(True)
rpb202.motionCtrl.setTimeStep(timeStep)
time.sleep(1)  # Let time for camera self ajustment
##rpb202 = robotBuilder.build()  # Dummy line for testing

##  Pointer to odometer
odometer = rpb202.odometer

lineTracker = rpb202.camera.lineTrackerBox
lineTracker.trackLines(fps)

maze = Maze()
startNode = maze.addNode(0, start = True)
startNode.setPos(0., 0.)

currNode = startNode
x, y, length = 0., 0., 0.
heading = 'E'
outHeading = heading
newPath = True

#####################
####  Testing...
##
##try:
##
##    while True:
##        speed = float(raw_input("speed: "))
##        dRead = float(raw_input("read int dist: "))
##        dInt = float(raw_input("int dist: ")) - dRead
##
##        print followLineToInt(speed)


try:

########################################################################
##  Explore Maze

    while maze.hasUnvisitedPaths():

        ##  Update heading
        heading = phiToHeading(odometer.getPhi())

        ##  Move to next corner/intersection
        prevNode = currNode
        inter = followLineToInt(speed)
##        inter = 5 # Dummy line for testing

        ##  Update pseudo odometry
        odometer.update()
        dx, dy = odometer.getPosXY()
##        dx, dy = 103, 10 # Dummy line for testing
        x, y, dist = correctedPos(x, y, dx, dy, heading)
        length += dist
        
        ##  Reset robot odometer
        odometer.resetPosXY()
        odometer.phi = headingToAngle(heading)

        ## Case of simple turn
        if inter == 1 or inter == 4:

            ##  Case of a left turn
            if inter == 1:
                heading = leftTurn(heading)
                turnToHeading(heading)

            ##  Case of a right turn
            elif inter == 4:
                heading = rightTurn(heading)
                turnToHeading(heading)

        ##  Case of intersection
        else:

            ##  If on a new node position            
            if newPath:
                currNode = maze.exploreNode(prevNode, x, y, nbPathsOut(inter), length, outHeading, heading)
                ##  If node is finish
                if inter == 8:
                    maze.setFinishNode(currNode)
                    finishNode = currNode

            ##  If moving to a previously visited node
            else:
                currNode = maze.getNodeAtPos(x, y)
                x, y = currNode.getPos()

            ##  Find next node with unvisited path and next heading
            nextNode = maze.getNextNodeToNearestUnvisited(currNode)

            if nextNode is currNode:
                ##  Current node has unvisited paths, heading to next unvisited path
                heading = nextUnvisitedHeading(currNode, heading, inter)
                newPath = True

            else:
                ##  Heading to previously visited node
                heading = maze.getHeadingToGoal(currNode, nextNode)
                newPath = False

            ##  Turn to heading
            turnToHeading(heading)
            
            outHeading = heading
            length = 0.


        # set newPath
        odometer.update()
        

########################################################################
##  Return to start by shortest path

########################################################################
##  Go to finish by shortest path



    ##  End of main loop, stop robot and threads
    rpb202.motionCtrl.stop()
    rpb202.camera.stop()
    lineTracker.stop()

except KeyboardInterrupt:

    rpb202.motionCtrl.stop()
    rpb202.camera.stop()
    lineTracker.stop()
    print "\nExiting program"
