from a_star import AStar
from Motors import *
from Sensors import *

class Robot:

    def __init__(self):
        self.aStar = AStar()
        self.motors = Motors(self.aStar)
        self.sensors = []
        self.buttons = []
        self.analog = [0, 0, 0, 0, 0, 0]

    def addSensor(self, sensorObj):
        self.sensors.append(sensorObj)

    def readSensors(self):
        for sensor in self.sensors:
            sensor.analog = self.analog[sensor.aPin]

    def readAStar(self):
        self.buttons = self.aStar.read_buttons()
        self.analog = self.aStar.read_analog()
        self.readSensors()

    def forward(self, speed):
        self.motors.forward(speed)

    def turn(self, rotSpeed):
        self.motors.turn(rotSpeed)

    def move(self, speed, rotSpeed):
        self.motors.speed(speed - rotSpeed, speed + rotSpeed) 

    def stop(self):
        self.motors.stop()
