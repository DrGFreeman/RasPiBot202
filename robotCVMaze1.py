print "Importing libraries"
import time
import robotBuilder
import PID

########################################
##  Functions

##  Turn robot
def turn(angle, dir = "L"):

    turnSpeed = .2
    fullTurn = 1.5
    if dir == "L":
        rpb202.turn(turnSpeed)
    elif dir == "R":
        rpb202.turn(-turnSpeed)
    time.sleep(fullTurn * angle / 360)
    rpb202.stop()
    time.sleep(tStep * 2)

##  Move robot to center of intersection after detection
def moveToIntersection(speed):

    rpb202.forward(speed)
    time.sleep(.25)  # Tuned for .25 / 2 fwd speed
    rpb202.stop()
    time.sleep(tStep * 2)

##  Move robot forward on line until intersection. Return configuration of intersection
def fwdOnLine(speed):
    
    while lineTracker.getNbLines() == 2:

        t0 = time.time()

        ##  Check if second line is on left -> perform left turn
        if lineTracker.getLinesHPos(1) < 8:
            print "Left corner detected"
            moveToIntersection(speed / 2.)
            turn(90, "L")
            
        ##  Else check if second line is on right -> perform right turn
        elif 192 < lineTracker.getLinesHPos(1):
            print "Right corner detected"
            moveToIntersection(speed / 2.)
            turn(90, "R")
            
        ##  Else move forward
        else:
            pid = PID.PID(.105, .03, .007)
            turn = -pid.getOutput(0, lineTracker.getLinesHPos(0), tStep)
            rpb202.move(speed, turn)

            ##  Finish time step
            dt = time.time() - t0
            if dt < tStep:
                time.sleep(tStep - dt)

    ##  Stop robot
    rpb202.stop()

    intersectionConfig = 0
    
    ##  Case of an intersection
    if lineTracker.getNbLines() > 2:
        print "Intersection detected"
        ##  Move fwd slightly to allow seeing all lines from intersection
        rpb202.forward(speed / 2.)
        time.sleep(.05)
        rpb202.stop()

    ##  Assess intersection configuration
    if lineTracker.getNbLines() == 3:
    ##  check if one line to left
        if lineTracker.getLinesHPos(1) < 8:
            "Left detected"
            intersectionConfig += 1
            ##  check if also one line on right -> "T" intersection
            if 192 < lineTracker.getLinesHPos(2):
                "Right detected"
                intersectionConfig += 4
            ##  If no right, there is one straight and one left
            else:
                "Straight detected"
                intersectionConfig += 2
        ##  Else there is one straight and one right
        else:
            print "Straight detected"
            print "Right detected"
            intersectionConfig += 6
            
    ##  Else it is a 4 way intersection
    elif lineTracker.getNbLines == 4:
        print "Four way detected"
        intersectionConfig += 7

    ##  Check if dead-end or finish
    if lineTracker.getNbLines() == 1:
        ##  Check if finish
        if lineTracker.getLinesAreaRatio(0) > .75:
            print "Finish reached"
            intersectionConfig = 8
        ##  Otherwise it is a dead-end
        else:
            intersectionConfig = 0
            print "Dead-end"
    ##  Else move to intersection
    else:
        moveToIntersection(speed / 2.)

    return intersectionConfig


##  Replace dead-ends by appropriate turns
def fixWrongTurns(turns):

    if len(turns) >= 3 and turns[-2] == "U":

        last3Turns = turns[-3] + turns[-2] + turns[-1]

        if defTurnDir == "L":
            if last3Turns == "LUL":
                newTurn = "S"
            elif last3Turns == "SUL" or last3Turns == "LUS":
                newTurn = "R"
            elif last3Turns == "RUL" or last3Turns == "SUS":
                newTurn = "U"

        elif defTurnDir == "R":
            if last3Turns == "RUR":
                newTurn = "S"
            elif last3Turns == "SUR" or last3Turns == "RUS":
                newTurn = "L"
            elif last3Turns == "LUR" or last3Turns == "SUS":
                newTurn = "U"

        turns[-3] = newTurn
        turns.pop()
        turns.pop()


########################################
##  Setup
        
##  Build Robot from robotBuilder (edit robotBuilder to customize robot)
print "Configuring robot"
rpb202 = robotBuilder.build(True)

##  Create direct pointer to camera object tracker
print "Connecting camera"
lineTracker = rpb202.camera.lineTracker
lineTracker.setDisplay(False)

##  Main loop time step
fps = 20.
tStep = 1 / fps

##  Default speed & turn direction
fwdSpeed = .25
defTurnDir = "L"

##  Launch object tracker
lineTracker.trackLines(fps)
time.sleep(1)

##  Storage of maze turns
mazeTurns = []

##  Main loop
print "Start maze learning"

try:

    ########################################
    ##  Learn maze
    
    finished = False
    while not finished:

        inter = fwdOnLine(fwdSpeed)
        
        ##  Case of a dead-end
        if inter == 1:
            turn(180, defTurnDir)
            mazeTurns.append("U")
        ##  Cases where default left turn can be made
        elif defTurnDir == "L" and (inter == 3 or inter == 5 or inter == 7):
            turn(90, defTurnDir)
            mazeTurns.append(defTurnDir)
        ##  Cases where default right turn can be made
        elif defTurnDir == "R" and (inter == 5 or inter == 6 or inter == 7):
            turn(90, defTurnDir)
            mazeTurns.append(defTurnDir)
        ##  Case where default left turn cannot be made
        elif defTurnDir == "L" and inter == 6:
            mazeTurns.append("S")
        ##  Case where default right turn cannot be made
        elif defTurnDir == "R" and inter == 3:
            mazeTurns.append("S")
        ##  Finish reached
        elif inter == 8:
            finished = True
            
        ##  Replace dead-ends by appropriate turns
        mazeTurns = fixWrongTurns(mazeTurns)

    ##  Learning completed
    print "Maze learning completed."
    raw_input("Replace robot at entry of maze and press any key to start optimized course")


    ########################################
    ##  Optimized course
    print "\nStarting optimized course"
    for turn in mazeTurns:

        fwdOnLIne(fwdSpeed)
        if turn == "L":
            print "Left turn"
            turn(90, "L")
        elif turn == "R":
            print "Right turn"
            turn(90, "R")
        else:
            print "Straight"

    print "Finished optimized course"


    ########################################
    ##  End of main loop. Stop robot and threads
    rpb202.stop()
    rpb202.camera.stop()
    lineTracker.stop()
        
##  Use Ctrl-C to end
except KeyboardInterrupt:
    rpb202.stop()
    rpb202.camera.stop()
    lineTracker.stop()
    print "\nExiting program"
    time.sleep(1)
