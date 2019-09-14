import re


def main():

    fileStr = readFiles()

    depth, target = getData(fileStr)

    grid = buildGrid(depth, target)
    
    riskLevel = calcRiskLevel(grid)

    print(riskLevel)


def calcRiskLevel(grid):
    return sum(map(sum, grid))


def buildGrid(depth, target):
    targetX = target[0]
    targetY = target[1]
    mod = 20183

    grid = [[0 for i in range(targetY + 1)] for i in range(targetX + 1)]

    # Calculate the grid after applying depth and erosion level modulo
    # Optimized so that actual large number multiplications do not take place
    for i in range(targetX + 1):
        for j in range(targetY + 1):
                
            indexVal = 0
            if (i == 0 and j == 0) or (i == targetX and j == targetY):
                indexVal = depth % mod
            elif i == 0:
                indexVal = (j * 16807 + depth) % mod
            elif j == 0:
                indexVal = (i * 48271 + depth) % mod
            else:
                indexVal = (grid[i - 1][j] * grid[i][j - 1] + depth) % mod

            grid[i][j] = indexVal

    # Get erosion level by modulo 3 to all numbers
    for i in range(targetX + 1):
        for j in range(targetY + 1):
            grid[i][j] %= 3

    return grid




def getData(fileStr):
    # Get the depth and target integers
    strList = fileStr.split('\n')
    depth = int(re.findall(r'\d+', strList[0])[0])
    target = re.findall(r'\d+', strList[1])
    targetY = int(target[0])
    targetX = int(target[1])
    target = [targetX, targetY]

    return depth, target


def readFiles():
    f = open('input.txt', 'r')
    fileStr = f.read()
    f.close()
    return fileStr


if __name__ == '__main__':
    main()
