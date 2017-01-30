class Encoders:

    def __init__(self):
        self.countLeft = 0
        self.countRight = 0
        self.lastCountLeft = 0
        self.lastCountRight = 0
        self.countSignLeft = 1
        self.countSignRight = -1

    def getCounts(self):
        return self.countLeft, self.countRight

    def setCounts(self, countLeft, countRight):

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
