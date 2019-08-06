import re
from collections import deque

def main():

    data = readFiles()

    highScore = runGame(data)

    print(highScore)


def runGame(data):
    numPlayers = int(data['numPlayers'])
    numMarbles = int(data['numMarbles'])

    scores = [0] * numPlayers
    circle = deque([0])

    for i in range(1, numMarbles + 1):
        player = i % numPlayers

        # Append marble
        if i % 23 != 0:
            circle.rotate(2)
            circle.append(i)

        # Remove marble
        else:
            circle.rotate(-7)
            score = circle.pop()

            scores[player] += i
            scores[player] += score

    return max(scores)


def readLine(line):
    pattern = re.compile(r"(?P<numPlayers>[0-9]+) players; last marble is worth (?P<numMarbles>[0-9]+) points")
    return pattern.match(line).groupdict()


def readFiles():
    data = None
    file = open("input2.txt", "r")

    for line in file:
        data = readLine(line)

    file.close()
    return data


if __name__ == "__main__":
    main()
