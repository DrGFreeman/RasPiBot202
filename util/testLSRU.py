from time import sleep

turnsList1 = ["L", "U", "L", "L", "S", "U", "L", "L", "U", "L", "L", "U", "L", "L", "L", "U", "L", "U", "L", "U", "L", "L"]
turnsList2 = ["R", "U", "R", "R", "U", "S", "R", "S", "S", "S"]

def substitute(mazeTurns):

    if len(mazeTurns) >= 3 and mazeTurns[-2] == "U":

        last3Turns = mazeTurns[-3] + mazeTurns[-2] + mazeTurns[-1]

        if defTurnDir == "L":
            if last3Turns == "LUL":
                newTurn = "S"
            elif last3Turns == "SUL" or last3Turns == "LUS":
                newTurn = "R"
            elif last3Turns == "RUL" or last3Turns == "SUS":
                newTurn = "U"

        elif defTurnDir == "R":
            if last3Turns == "RUR":
                newTurn = "S"
            elif last3Turns == "SUR" or last3Turns == "RUS":
                newTurn = "L"
            elif last3Turns == "LUR" or last3Turns == "SUS":
                newTurn = "U"
                
        mazeTurns[-3] = newTurn
        mazeTurns.pop()
        mazeTurns.pop()

    return mazeTurns

turns = []
defTurnDir = "L"

for turn in turnsList1:
    turns.append(turn)
    print turns
    turns = substitute(turns)
    print turns
    sleep(1)

print "\n"
turns = []
defTurnDir = "R"

for turn in turnsList2:
    turns.append(turn)
    print turns
    turns = substitute(turns)
    print turns
    sleep(1)
