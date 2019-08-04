import re
import datetime

def main():

    data = readFiles()

    highScore = runGame(data)

    print(highScore)


def runGame(data):
    numPlayers = int(data['numPlayers'])
    numMarbles = int(data['numMarbles'])

    scores = [0] * numPlayers
    circle = [0]
    curr = 0

    for i in range(1, numMarbles + 1):
        player = i % numPlayers

        # Append marble
        if i % 23 != 0:
            curr = getIdx(len(circle), curr, 2)

            if curr == 0:
                circle.append(i)
                curr = len(circle) - 1

            else:
                circle.insert(curr, i)

        # Remove marble
        else:
            curr = getIdx(len(circle), curr, -7)
            score = circle.pop(curr)
            
            if curr == len(circle):
                curr = 0

            scores[player] += i
            scores[player] += score

    return max(scores)


def getIdx(length, curr, offset):
    if offset < 0:
        offset = length + offset

    return (curr + offset) % length



def readLine(line):
    pattern = re.compile(r"(?P<numPlayers>[0-9]+) players; last marble is worth (?P<numMarbles>[0-9]+) points")
    return pattern.match(line).groupdict()


def readFiles():
    data = None
    file = open("input.txt", "r")

    for line in file:
        data = readLine(line)

    file.close()
    return data


if __name__ == "__main__":
    main()
