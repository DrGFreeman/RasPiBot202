# -*- coding: utf-8 -*-
import cwiid
import threading
import time

class WiiRemote:

    def __init__(self, n):
        self.btn1 = False
        self.btn2 = False
        self.btnA = False
        self.btnB = False
        self.btnC = False
        self.btnZ = False
        self.btnUp = False
        self.btnDown = False
        self.btnLeft = False
        self.btnRight = False
        self.id = id
        self.active = True
        self.wm = None
        self.stickH = 0
        self.stickV = 0

        # Connection à la manette Wii
        print "Appuyez simultamément les boutons 1 et 2 de la manette Wii maintenant"
        i = 1
        while not self.wm:
            try:
                self.wm = cwiid.Wiimote()
            except RuntimeError:
                if i > 10:
                    quit()
                    break
                print "Impossible de connecter le manette Wii"
                print "Tentative " + str(i)
                i += 1
        print "Manette Wii connectée avec succès"
        self.wm.led = n
        self.wm.rumble = True
        time.sleep(.2)
        self.wm.rumble = False
         
    def _robotRemote(self, freq):

        self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_NUNCHUK

        nunHRange = 222. - 22.
        nunHCenter = 122.
        nunVRange = 231. - 38.
        nunVCenter = 134.
        
        while self.active:
            buttons = self.wm.state['buttons']
            nunAcc = self.wm.state['nunchuk']['acc']
            nunButtons = self.wm.state['nunchuk']['buttons']
            nunStick = self.wm.state['nunchuk']['stick']
           
            nunStickH, nunStickV = nunStick

            self.stickH = (float(nunStickH) - nunHCenter) / nunHRange
            self.stickV = (float(nunStickV) - nunVCenter) / nunVRange
            
            if buttons & cwiid.BTN_A:
                self.btnA = True
            else:
                self.btnA = False
	    if nunButtons & cwiid.NUNCHUK_BTN_Z:
                self.btnZ = True
	    else:
                self.btnZ = False
            time.sleep(1 / freq)

    def _release(self):
        self.active = False
        print "Déconnection de la manette Wii\n"
        self.wm.rumble = True
        time.sleep(.2)
        self.wm.rumble = False
        self.wm.led = 0

    def robotRemote(self, freq):
        thread1 = threading.Thread(target = self._robotRemote, args = [freq])
        thread1.start()

    def release(self):
        if self.active:
            thread2 = threading.Thread(target = self._release, args = [])
            thread2.start()
                                              
    def setLed(self, led):
        self.wm.led = led

    def getLed(self):
        return self.wm.led
	
