class Encoders:

    def __init__(self, aStar):
        self.aStar = aStar
        self.countLeft = 0
        self.countRight = 0
        self.countSignLeft = 1
        self.countSignRight = 1
        self.aStar.reset_encoders()

    def getCounts(self):
        countLeft, countRight = self.aStar.read_encoders()
        self.aStar.reset_encoders()
        self.countLeft += self.countSignLeft * countLeft
        self.countRight += self.countSignRight * countRight
        return self.countLeft, self.countRight

    def reset(self):
        self.aStar.reset_encoders()
        self.countLeft = 0
        self.countRight = 0
