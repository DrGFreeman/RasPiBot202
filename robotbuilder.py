from robot import Robot
from sensors import *


def build(camera = False):

    ##  Create robot instance
    robot = Robot()

    ##  Create sensor calibration objects
    #   Sharp IR analog sensors
    calIR = SensCalPoly('IR-Sharp-GP2Y0A60SZLF', 40, 900, 1.734E3, -9.005E0, 2.023E-2, -2.251E-5, 1.167E-8, -2.037E-12)

    #   MaxBotix Sonar range finder
    #calSonar = SensCalPoly('Sonar-Maxbotix-XL-MaxSonar-EZ4-MB1240', 0, 765, 0, 10)

    ##  Create sensor objects
    irALeftOut = ADistSens('Left outboard analog IR', robot.analog, 0, calIR)
    irALeftIn = ADistSens('Left inboard analog IR', robot.analog, 2, calIR)
    irARightIn = ADistSens('Right inboard analog IR', robot.analog, 3, calIR)
    irARightOut = ADistSens('Right outboard analog IR', robot.analog, 4, calIR)
    #snrCtr = ADistSens('Center sonar', robot.analog, 5, calSonar)

    ## Add sensors to robot
    robot.addSensor(irALeftOut)
    robot.addSensor(irALeftIn)
    robot.addSensor(irARightIn)
    robot.addSensor(irARightOut)

    if camera:
        from camera import Camera
        robot.addCamera(Camera(2))

    return robot
