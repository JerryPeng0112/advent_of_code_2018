GRID_SERIAL_NUMBER = 6042
GRID_SIZE = 300


def main():
    grid = [[0 for i in range(GRID_SIZE)] for i in range(GRID_SIZE)]    

    populate(grid)

    sumAreaTable = createSumAreaTable(grid)

    x, y, size = calcMaxSquare(grid, sumAreaTable)
    print(str(x) + ',' + str(y) + ',' + str(size))


def populate(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = i + 1
            y = j + 1

            grid[i][j] = calcPower(x, y)


def calcPower(x, y):
    rackID = x + 10
    level = (rackID * y + GRID_SERIAL_NUMBER) * rackID
    return int(str(level)[-3]) - 5


def createSumAreaTable(grid):
    sumAreaTable = [[0 for i in range(GRID_SIZE)] for i in range(GRID_SIZE)]    

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):

            if i == 0 and j == 0:
                sumAreaTable[i][j] = grid[i][j]
            elif i == 0:
                sumAreaTable[i][j] = sumAreaTable[i][j - 1] + grid[i][j]
            elif j == 0:
                sumAreaTable[i][j] = sumAreaTable[i - 1][j] + grid[i][j]

            else:
                sumAreaTable[i][j] = sumAreaTable[i - 1][j] + sumAreaTable[i][j - 1]\
                        - sumAreaTable[i - 1][j - 1] + grid[i][j]

    return sumAreaTable



def calcMaxSquare(grid, sumAreaTable):
    maxPower = -1000000
    x = 0
    y = 0
    size = 0

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            powers = []

            for k in range(GRID_SIZE - max(i, j)):
                powers.append(calcAreaPower(sumAreaTable, i, j, k))

            if max(powers) > maxPower:
                maxPower = max(powers)
                x = i + 1
                y = j + 1
                size = powers.index(max(powers)) + 1

    return x, y, size


def calcAreaPower(sumAreaTable, x, y, size):
    # Calculate sum of a rectangular area based on sum area table
    if x == 0 and y == 0:
        return sumAreaTable[x + size][y + size]
    elif x == 0:
        return sumAreaTable[x + size][y + size] - sumAreaTable[x + size][y - 1]
    elif y == 0:
        return sumAreaTable[x + size][y + size] - sumAreaTable[x - 1][y + size]

    return sumAreaTable[x + size][y + size] - sumAreaTable[x - 1][y + size]\
            - sumAreaTable[x + size][y - 1] + sumAreaTable[x - 1][y - 1]


if __name__ == "__main__":
    main()
