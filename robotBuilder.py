from Robot import Robot
from Sensors import *

def build():

    ##  Create robot instance
    robot = Robot()

    ##  Create sensor calibration objects
    #   Sharp IR analog sensors
    calIR = SensCalPoly('IR-Sharp-GP2Y0A60SZLF', 40, 900, 1.734E3, -9.005E0, 2.023E-2, -2.251E-5, 1.167E-8, -2.037E-12)

    #   MaxBotix Sonar range finder
    calSonar = SensCalPoly('Sonar-Maxbotix-XL-MaxSonar-EZ4-MB1240', 0, 765, 0, 10)

    ##  Create sensor objects
    irALeft = ADistSens('Left analog IR', robot.analog, 2, calIR)
    irARight = ADistSens('Right analog IR', robot.analog, 3, calIR)
    irDLeft = DDistSens('Left digital IR', robot.analog, 0)
    irDRight = DDistSens('Right digital IR', robot.analog, 4)
    snrCtr = ADistSens('Center sonar', robot.analog, 5, calSonar)

    ## Add sensors to robot
    robot.addSensor(irDLeft)
    robot.addSensor(irALeft)
    robot.addSensor(snrCtr)
    robot.addSensor(irARight)
    robot.addSensor(irDRight)

    return robot
