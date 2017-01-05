import time
import cv2
import numpy as np
from picamera import PiCamera, PiCameraCircularIO
from SimpleCV import Image, ColorSpace

class Camera():
    
    def __init__(self, size=1, frameRate=40, hflip=False, vflip=False):
        self.active = False
        self.size = size
        self.hRes = size * 64
        self.vRes = size * 48
        self.picam = PiCamera()
        self.picam.resolution = (self.hRes, self.vRes)
        self.picam.framerate = frameRate
        self.picam.hflip = hflip
        self.picam.vflip = vflip
        time.sleep(2)
        self.stream = PiCameraCircularIO(self.picam, seconds=1)
        self.start()

    def close(self):
        self.stop()
        self.picam.close()

    def getOpenCVImage(self):
        img = np.empty((self.vRes * self.hRes * 3), dtype=np.uint8)
        self.picam.capture(img, 'bgr', use_video_port=True)
        img = img.reshape((self.vRes, self.hRes, 3))
        return img

    def getSimpleCVImage(self):
        img = np.empty((self.vRes * self.hRes * 3), dtype=np.uint8)
        self.picam.capture(img, 'bgr', use_video_port=True)
        img = img.reshape((self.vRes, self.hRes, 3))
        img = Image(img, colorSpace=ColorSpace.RGB)
        img = img.rotate90()
        img = img.flipVertical()
        return img

    def start(self):
        if not self.active:
            self.active = True
            self.picam.start_recording(self.stream, format='h264',
                                       resize=(self.hRes, self.vRes))
            
    def startPreview(self):
        self.picam.start_preview()

    def stop(self):
        self.active = False
        self.picam.stop_recording()
        self.stopPreview()

    def stopPreview(self):
        self.picam.stop_preview()
