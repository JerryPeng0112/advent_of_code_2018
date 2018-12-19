def main():

    data = readFiles()

    grid = makeOverlapGrid()
    mapOverlapGrid(data, grid)
    result = getIntactClaim(data, grid)

    print(result)

def makeOverlapGrid():
    return [[0 for x in range(1000)] for y in range(1000)]

def mapOverlapGrid(data, grid):
    for datum in data:
        for x in range(datum["startX"], datum["endX"]):
            for y in range(datum["startY"], datum["endY"]):

                if grid[x][y] == 0:
                    grid[x][y] = 1
                elif grid[x][y] == 1:
                    grid[x][y] = 2

def getIntactClaim(data, grid):
    for datum in data:
        intact = True
        for x in range(datum["startX"], datum["endX"]):
            for y in range(datum["startY"], datum["endY"]):
                if grid[x][y] == 2:
                    intact = False
        if intact:
            return datum["id"]
                

def processFileLine(line):
    data = {}
    lineSplit = line.split()
    startCoor = lineSplit[2].split(',')
    startCoor[1] = startCoor[1][:-1]
    dim = line.split()[3].split('x')
    data["id"] = int(lineSplit[0][1:])
    data["startX"] = int(startCoor[0])
    data["startY"] = int(startCoor[1])
    data["endX"] = data["startX"] + int(dim[0])
    data["endY"] = data["startY"] + int(dim[1])
    return data

def readFiles():
    data = []
    file = open("input.txt", "r")
    for line in file:
        data.append(processFileLine(line))
    return data

if __name__ == "__main__":
    main()
