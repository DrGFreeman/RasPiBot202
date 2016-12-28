import time

# A simple, multi-purpose timer class to manage time steps in loops, control execution times, etc.
class Timer:

    # Constructor starts the timer at instantiation
    def __init__(self):
        self.paused = False
        self.pauseInitTime = []
        self.pauseElapsed = 0
        self.initTime = time.time()


    # Method resets the timer initial time to current time
    def reset(self):
        self.paused = False
        self.pauseInitTime = []
        self.pauseElapsed = 0
        self.initTime = time.time()

    # Method allows to pause the timer
    def pause(self):
        self.pauseInitTime = time.time()
        self.paused = True

    # Method allows to resume counting time following call to Timer.pause()
    def resume(self):
        if self.paused:
            self.pauseElapsed += time.time() - self.pauseInitTime
            self.paused = False
        else:
            print "Timer.resume() called without prior call to Timer.pause()"

    # Method returns the time elapsed since instantiation or last reset minus sum of paused time
    def getElapsed(self):
        if self.paused:
            return self.pauseInitTime - self.initTime - self.pauseElapsed
        else:
            return time.time() - self.initTime - self.pauseElapsed

    # Method sleeps until elapsed time reaches delay argument then resets the timer
    # Useful to control fixed time step in loops.
    def sleepToElapsed(self, delay):
        if self.getElapsed() < delay:
            time.sleep(delay - self.getElapsed())
        self.reset()

    # Method returns True if elapsed time is within delay argument.
    # Useful to control execution of while loops for a fixed time duration.
    def isWithin(self, delay):
        if self.getElapsed() <= delay:
            return True
        else:
            return False
