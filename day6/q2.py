from enum import Enum

DISTANCE = 10000

class Para(Enum):
    XMIN = 0
    YMIN = 1
    XMAX = 2
    YMAX = 3


def main():

    data = readFiles()
    parameter = getParameter(data)

    area = getArea(data, parameter)
    print(area)


def getParameter(data):
    parameter = []
    xCoor = list(map(lambda x: x[0], data)) 
    yCoor = list(map(lambda x: x[1], data)) 
    parameter.append(min(xCoor))
    parameter.append(min(yCoor))
    parameter.append(max(xCoor))
    parameter.append(max(yCoor))
    return parameter


def getArea(data, parameter):
    xStart = int((parameter[Para.XMIN.value] + parameter[Para.XMAX.value]) / 2)
    yStart = int((parameter[Para.YMIN.value] + parameter[Para.YMAX.value]) / 2)
    area = 0

    xCurr = xStart
    while getTotalDist(xCurr, yStart, data) < DISTANCE:

        yCurr = yStart
        while getTotalDist(xCurr, yCurr, data) < DISTANCE:
            area += 1
            yCurr += 1

        yCurr = yStart - 1
        while getTotalDist(xCurr, yCurr, data) < DISTANCE:
            area += 1
            yCurr -= 1

        xCurr += 1

    xCurr = xStart - 1
    while getTotalDist(xCurr, yStart, data) < DISTANCE:

        yCurr = yStart
        while getTotalDist(xCurr, yCurr, data) < DISTANCE:
            area += 1
            yCurr += 1

        yCurr = yStart - 1
        while getTotalDist(xCurr, yCurr, data) < DISTANCE:
            area += 1
            yCurr -= 1

        xCurr -= 1

    return area


def getTotalDist(x, y, data):
    dists = []

    for d in data:
        dists.append(mhtDist(x, y, d[0], d[1]))

    return sum(dists)


# Get manhatton distance
def mhtDist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def readLine(line):
    return list(map(int, line.strip().split(',')))


def readFiles():
    data = []
    file = open("input.txt", "r")

    for line in file:
        data.append(readLine(line))
    
    file.close()
    return data


if __name__ == "__main__":
    main()
