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

    turnCorr = .1 * lineTracker.getBtmHPos()
    while abs(turnCorr) > .1:
        print turnCorr
        rpb202.turn(turnCorr)
        time.sleep(tStep)
        turnCorr = .1 * lineTracker.getBtmHPos()
    
    time.sleep(tStep * 2)

##  Move robot to center of intersection after detection
def moveToIntersection(speed):

    pid = PID.PID(.1)

    t0 = time.time()

    while time.time() - t0 < fwd2 - fwd1:

        t1 = time.time()
        
        turnCorr = -pid.getOutput(0, lineTracker.getBtmHPos(), tStep)
        rpb202.move(speed, turnCorr)

        dt = time.time() - t1
        if dt < tStep:
            time.sleep(tStep - dt)

    rpb202.stop()
    #time.sleep(tStep * 2)

##  Move robot forward on line until intersection. Return configuration of intersection
def fwdOnLine(speed):

    pid = PID.PID(.1, .05)

    finished = False
    while not finished:
        
        ##  Follow line until intersection is found    
        while lineTracker.getIntersection() == 2:

            t0 = time.time()

            turnCorr = -pid.getOutput(0, lineTracker.getBtmHPos(), tStep)
            rpb202.move(speed, turnCorr)

            dt = time.time() - t0
            if dt < tStep:
                time.sleep(tStep - dt)

        ##  At intersection move forward slightly
        rpb202.move(speed, 0)
        time.sleep(fwd1)
        rpb202.stop()

        intersection = lineTracker.getIntersection()
        #print "Capture"

        moveToIntersection(speed)

        ##  Case of a left turn
        if intersection == 1:
            turn(90, "L")
        elif intersection == 4:
            turn(90, "R")
        else:
            finished = True

    return intersection

    

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

    return turns


########################################
##  Setup
        
##  Build Robot from robotBuilder (edit robotBuilder to customize robot)
print "Configuring robot"
rpb202 = robotBuilder.build(True)

##  Create direct pointer to camera object tracker
print "Connecting camera"
lineTracker = rpb202.camera.lineTrackerBox

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

    fwd1 = .45
    fwd2 = 1.55
    turn1 = 4.55#4.55

    finished = False
    while not finished:

        inter = fwdOnLine(fwdSpeed)
        print "Intersection code: ", inter

        ##  Case of a dead-end
        if inter == 0:
            turn(180, defTurnDir)
            mazeTurns.append("U")
        ##  Case of a left turn
        elif inter == 1:
            turn(90, "L")
        ##  Case of a right turn
        elif inter == 4:
            turn(90, "R")
        ##  Cases where default left turn can be made
        elif defTurnDir == "L" and (inter == 3 or inter == 5 or inter == 7):
            turn(90, defTurnDir)
            mazeTurns.append("L")
        ##  Cases where default right turn can be made
        elif defTurnDir == "R" and (inter == 5 or inter == 6 or inter == 7):
            turn(90, defTurnDir)
            mazeTurns.append("R")
        ##  Case where default left turn cannot be made
        elif defTurnDir == "L" and inter == 6:
            mazeTurns.append("S")
        ##  Case where default right turn cannot be made
        elif defTurnDir == "R" and inter == 3:
            mazeTurns.append("S")
        ##  Finish reached
        elif inter == 8:
            finished = True

        print mazeTurns
            
        ##  Replace dead-ends by appropriate turns
        mazeTurns = fixWrongTurns(mazeTurns)
        print mazeTurns

    ##  Learning completed
    print "Maze learning completed."
    raw_input("Replace robot at entry of maze and press any key to start optimized course")


    ########################################
    ##  Optimized course
    print "\nStarting optimized course"

    fwdOnLine(fwdSpeed)
    for mazeTurn in mazeTurns:

        if mazeTurn == "L":
            print "Left turn"
            turn(90, "L")
        elif mazeTurn == "R":
            print "Right turn"
            turn(90, "R")
        else:
            print "Straight"
            
        fwdOnLine(fwdSpeed)

    print "Finished optimized course"


##        turn(180, defTurnDir)
##
##        print "\nCurrent time for intersection detection: ", fwd1
##        fwd1 = raw_input("Enter new time for intersection detection: ")
##        print "\nCurrent time for move to intersection: ", fwd2
##        fwd2 = raw_input("Enter new time for move to intersection: ")
##        print "\nCurrent time for full turn: ", turn1
##        turn1 = raw_input("Enter new time for full turn: ")
##
##        if fwd1 == "q" or fwd2 == "q":
##            end = True
##        else:
##            fwd1 = float(fwd1)
##            fwd2 = float(fwd2)
##            turn1 = float(turn1)


    ########################################
    ##  End of main loop. Stop robot and CV threads
    rpb202.stop()
    rpb202.camera.stop()
    lineTracker.stop()
    time.sleep(2 * tStep)
        
##  Use Ctrl-C to end
except KeyboardInterrupt:
    rpb202.stop()
    rpb202.camera.stop()
    lineTracker.stop()
    print "\nExiting program"
    time.sleep(2 * tStep)
