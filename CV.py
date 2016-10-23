import threading
import time

import SimpleCV

class Camera:

    def __init__(self):
        self.camera = SimpleCV.Camera()
        self.objTracker = ObjTracker(self.camera)
        self.display = False

    def _show(self, freq):

        self.display = True

        while self.display:

            t0 = time.time()

            img = self.camera.getImage()   

            topCropH = 60
            img = img.resize(w = 200)
            img = img.crop(0, topCropH, img.width, img.height - topCropH)
            img.show()

            dt = time.time() - t0
            if dt < 1 / freq:
                time.sleep(1 / freq -dt)

    def show(self, freq = 10):
        th = threading.Thread(target = self._show, args = [freq])
        th.start()

    def stop(self):
        self.display = False

class ObjTracker:

    def __init__(self, camera):
        self.camera = camera
        self.display = True
        self.active = False
        self.nbObj = 0
        self.objHPos = []
        self.objVPos = []
        self.objAreaRatio = []

    def _trackObjByHue(self, hue, freq):

##        cam = SimpleCV.Camera()

        self.active = True
        
        while self.active:

            t0 = time.time()
            
            img = self.camera.getImage()   

            topCropH = 60
            img = img.resize(w = 200)
            img = img.crop(0, topCropH, img.width, img.height - topCropH)

            col = SimpleCV.Color.hueToBGR(hue)
            iBin = img.hueDistance(color = col, minsaturation = 150).binarize(40)

            blobs = iBin.findBlobs()

            if blobs is not None:
                self.nbObj = 1
                blobs.sortArea()
                obj = blobs[0]
                x, y = obj.centroid()
                self.objHPos = (img.width / 2 - x) / (img.width / 2) # Inverse x axis so positive value corresponds to positive rotation in robot coord system
                self.objVPos = (y - img.height / 2) / (img.height / 2)
                self.objAreaRatio = obj.area() / img.area()
                if self.display:
                    dl = img.dl()
                    obj.drawRect(layer = dl, color = (0, 255, 0), width = 2)
            else:
                self.nbObj = 0
                self.objHPos = []
                self.objVPos = []
                self.objAreaRatio = []

            if self.display:
                img.show()

            dt = time.time() - t0
            if dt < 1 / freq:
                time.sleep(1 / freq -dt)

    def trackObjByHue(self, hue, freq = 10):
        th = threading.Thread(target = self._trackObjByHue, args = (hue, freq))
        th.start()

    def stop(self):
        self.active = False
        self.nbObj = 0
        self.objHPos = []
        self.objVPos = []
        self.objAreaRatio = []

    def hasObj(self):
        if self.nbObj > 0:
            return True
        else:
            return False

    def getObjHPos(self):
        return self.objHPos

    def getObjVPos(self):
        return self.objVPos

    def getObjAreaRatio(self):
        return self.objAreaRatio

    def setDisplay(self, display):
        self.display = display
