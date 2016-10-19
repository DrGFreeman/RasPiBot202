from time import sleep

from a_star import AStar

from Robot import Motors

aStar = AStar()
motors = Motors(aStar)

try:
    
    nFaces = 4

    tTurn = 1.543
    tFwd = 3

    spdTurn = -.5
    spdFwd = .3

    for i in range(nFaces):
        motors.forward(spdFwd)
        sleep(tFwd)
        motors.stop()
        motors.turn(spdTurn)
        sleep(tTurn / nFaces)
        motors.stop()


    motors.stop()

except KeyboardInterrupt:
    motors.stop()

