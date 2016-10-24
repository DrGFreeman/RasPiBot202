from SimpleCV import *
import time

cam = Camera()

try:
    while True:

        t0 = time.time()
        
        img = cam.getImage()   

        topCropH = 60
        img = img.resize(w = 200)
        img = img.crop(0, topCropH, img.width, img.height - topCropH)

    ##    img.show()
    ##    time.sleep(.5)

        jaune = Color.hueToBGR(74)
        iBin = img.hueDistance(color = jaune, minsaturation = 150)
        iBin = iBin.binarize(40)
    ##    iBin.show()
    ##    time.sleep(.5)

        blobs = iBin.findBlobs()
##        iBin.show()
##        blobs.show()
##        print blobs

        if blobs is not None:
            blobs.sortArea()
            verre = blobs[0]
            x, y = verre.centroid()
            print x - img.width / 2
            dl = img.dl()
            verre.drawRect(layer = dl, color = (0, 255, 0), width = 2)

        img.show()

        dt = time.time() - t0
        if dt < .1:
            time.sleep(.1 -dt)    ##    time.sleep(3)

except KeyboardInterrupt:
    print "Fin"

