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

    def _map2mcpi(self, freq):

        import pyautogui as pag

        self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_NUNCHUK
        
        while self.active:
            buttons = self.wm.state['buttons']
            nunAcc = self.wm.state['nunchuk']['acc']
            nunButtons = self.wm.state['nunchuk']['buttons']
            nunStick = self.wm.state['nunchuk']['stick']
            if buttons & cwiid.BTN_UP:
                pag.keyDown('w')
            else:
                pag.keyUp('w')
            if buttons & cwiid.BTN_DOWN:
                pag.keyDown('s')                
            else:
                pag.keyUp('s')

            if buttons & cwiid.BTN_LEFT:
                pag.keyDown('a')                
            else:
                pag.keyUp('a')
            if buttons & cwiid.BTN_RIGHT:
                pag.keyDown('d')                
            else:
                pag.keyUp('d')
            if nunButtons & cwiid.NUNCHUK_BTN_C:
                pag.keyDown('space')
            else:
                pag.keyUp('space')
##	    if buttons & cwiid.BTN_1:
##                slef.btn1 = True
##            else:
##                self.btn1 = False
##            if buttons & cwiid.BTN_2:
##                self.btn2 = True
##            else:
##                self.btn2 = False
##
##            if buttons & cwiid.BTN_A:
##		self.btnA = True
##            else:
##                self.btnA = False
##            if buttons & cwiid.BTN_B:
##		self.btnB = True
##            else:
##                self.btnB = False
##            if buttons & cwiid.BTN_UP:
##                self.btnUp = True
##            else:
##                self.btnUp = False
##            if buttons & cwiid.BTN_DOWN:
##                self.btnDown = True
##            else:
##                self.btnDown = False
##
##            if buttons & cwiid.BTN_LEFT:
##		self.btnLeft = True
##            else:
##                self.btnLeft = False
##            if buttons & cwiid.BTN_RIGHT:
##		self.btnRight = True
##            else:
##                self.btnRight = False
##            if nunButtons & cwiid.NUNCHUK_BTN_C:
##                self.btnC = True
##            else:
##                self.btnC = False
##	    if nunButtons & cwiid.NUNCHUK_BTN_Z:
##                self.btnZ = True
##	    else:
##                self.btnZ = False
##            time.sleep(1/freq)
            
    def _robotRemote(self, freq):

        self.wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_NUNCHUK
        
        while self.active:
            buttons = self.wm.state['buttons']
            nunAcc = self.wm.state['nunchuk']['acc']
            nunButtons = self.wm.state['nunchuk']['buttons']
            nunStick = self.wm.state['nunchuk']['stick']
            
            self.stickH, self.stickV = nunStick
            if buttons & cwiid.BTN_A:
                self.btnA = True
            else:
                self.btnA = False
            time.sleep(1 / freq)

    def _release(self):
        self.active = False
        print "Déconnection de la manette Wii\n"
        self.wm.rumble = True
        time.sleep(.2)
        self.wm.rumble = False
        self.wm.led = 0

    def map2mcpi(self, freq):
        thread1 = threading.Thread(target = self._map2mcpi, args = [freq])
        thread1.start()

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
	
