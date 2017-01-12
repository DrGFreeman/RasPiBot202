class Encoders:

    def __init__(self, aStar):
        self.aStar = aStar
        self.countLeft = 0
        self.countRight = 0
        self.lastCountLeft = 0
        self.lastCountRight = 0
        self.countSignLeft = 1
        self.countSignRight = -1
        self.aStar.reset_encoders()

    def readCounts(self):
        countLeft, countRight = self.aStar.read_encoders()

        diffLeft = (countLeft - self.lastCountLeft) % 0x10000
        if diffLeft >= 0x8000:
            diffLeft -= 0x10000
            
        diffRight = (countRight - self.lastCountRight) % 0x10000
        if diffRight >= 0x8000:
            diffRight -= 0x10000
            
        self.countLeft += self.countSignLeft * diffLeft
        self.countRight += self.countSignRight * diffRight

        self.lastCountLeft = countLeft
        self.lastCountRight = countRight
        
        return self.countLeft, self.countRight

    def reset(self):
        self.countLeft = 0
        self.countRight = 0
