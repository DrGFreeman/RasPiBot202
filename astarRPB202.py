import smbus
import struct
import threading
import time
from timer import Timer

class AStar(object):

    def __init__(self, encoders, odometer):
        self._bus = smbus.SMBus(1)
    	self.btnA = False
    	self.btnB = False
    	self.btnC = False
    	self.ledRed = False
    	self.ledYellow = False
    	self.ledGreen = False
    	self._notes = ''
    	self._motorLeft = 0
    	self._motorRight = 0
    	self.batteryMilliVolts = 0
    	self.analog = [0, 0, 0, 0, 0, 0]
    	self._encReset = True
        self.encoders = encoders
        self.odometer = odometer
        self.pan = 6000
        self.tilt = 6000
        self.mast = 6000
    	self.run()

    def _read_unpack(self, address, size, format):
    	self._bus.write_byte(20,address)
    	time.sleep(.0001)
    	byte_list = []
    	for n in range(0,size):
    	  byte_list.append(self._bus.read_byte(20))
    	return struct.unpack(format,bytes(bytearray(byte_list)))

    def _write_pack(self, address, format, *data):
    	data_array = map(ord, list(struct.pack(format, *data)))
    	self._bus.write_i2c_block_data(20, address, data_array)
    	time.sleep(.0001)

    def kill(self):
        ##  Stop running thread
        self._active = False
        ##  Reset motor values
        self._motorLeft, self._motorRight = 0, 0
        self._write_pack(6, 'hh', self._motorLeft, self._motorRight)
        ##  Turn leds off
        self.leds(0, 0, 0)
        self._write_pack(0, 'BBB', self.ledYellow, self.ledGreen, self.ledRed)

    def _run(self):
        ##  Runs continuously until self.active is set to False
        while self._active:
            try:
                ##  Read from buffer

                ##  Buttons
                self.btnA, self.btnB, self.btnC = self._read_unpack(3, 3, "???")
                ##  Battery
                self.batteryMilliVolts = self._read_unpack(10, 2, "H")[0]
                ##  Analog
                self.analog = self._read_unpack(12, 12, "HHHHHH")
                ##  Encoders
                counts = self._read_unpack(25, 4, "hh")
                self.encoders.setCounts(counts[0], counts[1])
                ##  Update odometer with latest encoder counts
                self.odometer.update(time.time())

                ##  Write to buffer

                ##  Leds
                self._write_pack(0, 'BBB', self.ledYellow, self.ledGreen,
                                 self.ledRed)
                ##  Motors
                self._write_pack(6, 'hh', self._motorLeft, self._motorRight)
                if self._encReset:
                    ##  Set flag to reset encoders
                    self._write_pack(24, 'B', 1)
                    self._encReset = False
                if self._notes != '':
                    ##  Play notes
                    self._write_pack(29, 'B15s', 1, self._notes.encode("ascii"))
                    self._notes = ''
                ##  Servos
                self._write_pack(44, 'HHH', self.pan, self.tilt, self.mast)

            ##  Handle I2C communication error
            except IOError:
                raise IOError("IOError in AStar class")
                self.kill()

            time.sleep(.009)

    def run(self):
        self._active = True
        th = threading.Thread(target=self._run, args = [])
        th.start()

    def leds(self, yellow, green, red):
        self.ledRed = red
        self.ledYellow = yellow
        self.ledGreen = green

    def play_notes(self, notes):
        self._notes = notes

    def motors(self, left, right):
        self._motorLeft, self._motorRight = left, right

    def read_buttons(self):
        return self.btnA, self.btnB, self.btnC

    def read_battery_millivolts(self):
        return self.batteryMilliVolts

    def read_analog(self):
        return self.analog

    def reset_encoders(self):
        self.resetEncoders = True

    def test_read8(self):
    	self._read_unpack(0, 8, 'cccccccc')

    def test_write8(self):
    	self._bus.write_i2c_block_data(20, 0, [0,0,0,0,0,0,0,0])
    	time.sleep(.0001)
