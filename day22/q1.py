import re


def main():

    fileStr = readFiles()

    depth, target = getData(fileStr)

    eroLevelTable = buildEroLevelTable(depth, target)
    
    riskLevel = calcRiskLevel(eroLevelTable)

    print(riskLevel)


def calcRiskLevel(eroLevelTable):
    return sum(map(sum, eroLevelTable))


def buildEroLevelTable(depth, target):
    targetX = target[0]
    targetY = target[1]
    mod = 20183

    table = [[0 for i in range(targetX + 1)] for i in range(targetY + 1)]

    # Calculate the table after applying depth and erosion level modulo
    # Optimized so that actual large number multiplications do not take place
    for i in range(targetY + 1):
        for j in range(targetX + 1):
                
            indexVal = 0
            if (i == 0 and j == 0) or (i == targetY and j == targetX):
                indexVal = depth % mod
            elif i == 0:
                indexVal = (j * 16807 + depth) % mod
            elif j == 0:
                indexVal = (i * 48271 + depth) % mod
            else:
                indexVal = (table[i - 1][j] * table[i][j - 1] + depth) % mod

            table[i][j] = indexVal

    # Get erosion level by modulo 3 to all numbers
    for i in range(targetY + 1):
        for j in range(targetX + 1):
            table[i][j] %= 3

    return table




def getData(fileStr):
    # Get the depth and target integers
    strList = fileStr.split('\n')
    depth = int(re.findall(r'\d+', strList[0])[0])
    target = re.findall(r'\d+', strList[1])
    targetX = int(target[0])
    targetY = int(target[1])
    target = [targetX, targetY]

    return depth, target


def readFiles():
    f = open('input.txt', 'r')
    fileStr = f.read()
    f.close()
    return fileStr


if __name__ == '__main__':
    main()
