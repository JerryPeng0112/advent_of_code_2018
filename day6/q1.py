from enum import Enum

class Para(Enum):
    XMIN = 0
    YMIN = 1
    XMAX = 2
    YMAX = 3


def main():

    data = readFiles()
    parameter = getParameter(data)

    validCoors = getValidCoor(data, parameter)
    areas = calcAreas(data, parameter)

    validIndices = list(filter(lambda x: validCoors[x] == 1, range(len(data))))
    maxAreas = max(map(lambda x: areas[x], validIndices))
    print(maxAreas)


def getParameter(data):
    parameter = []
    xCoor = list(map(lambda x: x[0], data)) 
    yCoor = list(map(lambda x: x[1], data)) 
    parameter.append(min(xCoor))
    parameter.append(min(yCoor))
    parameter.append(max(xCoor))
    parameter.append(max(yCoor))
    return parameter


def getValidCoor(data, parameter):
    validCoors = [1] * len(data)

    # If any coordinates are closest to borders, they are invalidated
    for i in range(parameter[Para.XMIN.value] - 1, parameter[Para.XMAX.value] + 2):
        idx1 = getClosestIndex(i, parameter[Para.YMIN.value] - 1, data)
        idx2 = getClosestIndex(i, parameter[Para.YMAX.value] + 1, data)
        validateCoor(idx1, validCoors)
        validateCoor(idx2, validCoors)


    for i in range(parameter[Para.YMIN.value] - 1, parameter[Para.YMAX.value] + 2):
        idx1 = getClosestIndex(parameter[Para.XMIN.value] - 1, i, data)
        idx2 = getClosestIndex(parameter[Para.XMAX.value] + 1, i, data)
        validateCoor(idx1, validCoors)
        validateCoor(idx2, validCoors)

    return validCoors


def calcAreas(data, parameter):
    areas = [0] * len(data)

    for i in range(parameter[Para.XMIN.value], parameter[Para.XMAX.value] + 1):
        for j in range(parameter[Para.YMIN.value], parameter[Para.YMAX.value] + 1):
            idx = getClosestIndex(i, j, data)

            if idx != -1:
                areas[idx] += 1

    return areas

def getClosestIndex(x, y, data):
    dists = []
    for d in data:
        dists.append(mhtDist(x, y, d[0], d[1]))

    indices = list(filter(lambda x: dists[x] == min(dists), range(len(dists))))
    
    if len(indices) == 1:
        return indices[0]
    else:
        return -1


def validateCoor(idx, validCoors):
    if idx != -1:
        validCoors[idx] = 0


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
