print "Importing libraries"
import time
import robotBuilder
import PID

########################################
##  Functions

##  Turn robot
def turn(angle, dir = "L"):

    turnSpeed = .25
    fullTurn = turn1
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
    time.sleep(fwd2 - fwd1)  # Tuned for .25 / 2 fwd speed
    rpb202.stop()
    time.sleep(tStep * 2)

##  Move robot forward on line until intersection. Return configuration of intersection
def fwdOnLine(speed):

    pid = PID.PID(.05)
    
    while lineTracker.getNbLines() == 2:

        t0 = time.time()

        hPos = []
        for line in lineTracker.linesHPos:
            hPos.append(line)
        print hPos

        ##  Check if second line is on left -> perform left turn
        if .8 < lineTracker.getLinesHPos(1):
            print "Left corner detected"
            moveToIntersection(speed)
            turn(90, "L")
            pid.reset()
            
        ##  Else check if second line is on right -> perform right turn
        elif lineTracker.getLinesHPos(1) < -.8:
            print "Right corner detected"
            moveToIntersection(speed)
            turn(90, "R")
            pid.reset()
            
        ##  Else move forward
        #else:
        turnCorr = -pid.getOutput(0, lineTracker.getLinesHPos(0), tStep)
        rpb202.move(speed, turnCorr)

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
        rpb202.forward(speed)
        time.sleep(fwd1)
        rpb202.stop()
        for line in lineTracker.linesHPos:
            hPos.append(line)
        print hPos

    ##  Assess intersection configuration
    if lineTracker.getNbLines() == 3:
    ##  check if one line to left
        if .8 < lineTracker.getLinesHPos(1):
            "Left detected"
            intersectionConfig += 1
            ##  check if also one line on right -> "T" intersection
            if lineTracker.getLinesHPos(2) < -.8:
                "Right detected"
                intersectionConfig += 4
            ##  If no right, there is one straight and one left
            else:
                "Straight detected"
                intersectionConfig += 2
        ##  Else there is one straight and one right
        else:
            print "Straight and Right detected"
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
        moveToIntersection(speed)

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
lineTracker.setDisplay(True)

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

print "Start main"

try:

    fwd1 = 0.
    fwd2 = 1.45
    turn1 = 4.5

    end = False
    while not end:

        inter = fwdOnLine(fwdSpeed)
        print "Intersection code: ", inter
        turn(180, defTurnDir)

        print "\nCurrent time for intersection detection: ", fwd1
        fwd1 = raw_input("Enter new time for intersection detection: ")
        print "\nCurrent time for move to intersection: ", fwd2
        fwd2 = raw_input("Enter new time for move to intersection: ")
        print "\nCurrent time for full turn: ", turn1
        turn1 = raw_input("Enter new time for full turn: ")

        if fwd1 == "q" or fwd2 == "q":
            end = True
        else:
            fwd1 = float(fwd1)
            fwd2 = float(fwd2)
            turn1 = float(turn1)


    ########################################
    ##  End of main loop. Stop robot and CV threads
    rpb202.stop()
    rpb202.camera.stop()
    lineTracker.stop()
        
##  Use Ctrl-C to end
except KeyboardInterrupt as e:
    rpb202.stop()
    rpb202.camera.stop()
    lineTracker.stop()
    print "\nExiting program"
