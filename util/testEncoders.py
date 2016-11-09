import time
from a_star_rpb202 import AStar

a = AStar()

i = 0

while True:
    print a.read_encoders()
    time.sleep(.5)
    if i == 10:
        a.reset_encoders()
        i = 0
    i += 1
