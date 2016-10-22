import threading
import time

from SimpleCV import *

class TrackObj:

    def __init__(self):
        self.active = False
        self.hasObj = False

    def _trackObjByHue(self, hue, freq):

        cam = Camera()

        self.active = True
        
        while self.active:

            t0 = time.time()
            
            img = cam.getImage()   

            topCropH = 60
            img = img.resize(w = 200)
            img = img.crop(0, topCropH, img.width, img.height - topCropH)

            col = Color.hueToBGR(hue)
            iBin = img.hueDistance(color = col, minsaturation = 150).binarize(40)

            blobs = iBin.findBlobs()

            if blobs is not None:
                self.hasObj = True
                blobs.sortArea()
                obj = blobs[0]
                x, y = obj.centroid()
                hPos = (img.width / 2 - x) / (img.width / 2)
                areaPct = obj.area() / img.area()
                dl = img.dl()
                obj.drawRect(layer = dl, color = (0, 255, 0), width = 2)
            else:
                self.hasObj = False

            img.show()

            dt = time.time() - t0
            if dt < 1 / freq:
                time.sleep(1 / freq -dt)

            return self.hasObj, hPos, areaPct, 

    def trackObjByHue(self, hue, freq):
        th = threading.Thread(target = _trackObjByHue, args = (hue, freq))
        th.start()

    def stop():
        self.active = False
        self.hasObj = False
