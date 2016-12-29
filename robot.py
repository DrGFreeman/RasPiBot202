from astarRPB202 import AStar
from encoders import Encoders
from motioncontroller import MotionController
from motors import Motors
from odometer import Odometer
from pantilt import PanTilt

class Robot:

    def __init__(self):
        self.aStar = AStar()
        self.encoders = Encoders(self.aStar)
        self.odometer = Odometer(self.encoders)
        self.motors = Motors(self.aStar, self.encoders, self.odometer)
        self.motionCtrl = MotionController(self.odometer, self.motors)
        self.sensors = []
        self.buttons = []
        self.analog = [0, 0, 0, 0, 0, 0]
        self.camera = []
        self.panTilt = PanTilt(18, 12)

    def addSensor(self, sensorObj):
        self.sensors.append(sensorObj)

    def readSensors(self):
        for sensor in self.sensors:
            sensor.analog = self.analog[sensor.aPin]

    def addCamera(self, camera):
        self.camera = camera

    def readAStar(self):
        self.buttons = self.aStar.read_buttons()
        self.analog = self.aStar.read_analog()
        self.readSensors()

    def forward(self, speed):
        self.motors.forward(speed)

    def turn(self, rotSpeed):
        self.motors.turn(rotSpeed)

    def move(self, speed, rotSpeed):
        self.motors.cmd(speed - rotSpeed, speed + rotSpeed) 

    def stop(self):
        self.motionCtrl.stop()
