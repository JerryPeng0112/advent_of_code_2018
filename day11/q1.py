GRID_SERIAL_NUMBER = 6042


def main():
    grid = [[0 for i in range(300)] for i in range(300)]    

    populate(grid)

    x, y = calcMaxSquare(grid)
    print(str(x) + ',' + str(y))


def populate(grid):
    for i in range(300):
        for j in range(300):
            x = i + 1
            y = j + 1

            grid[i][j] = calcPower(x, y)


def calcPower(x, y):
    rackID = x + 10
    level = (rackID * y + GRID_SERIAL_NUMBER) * rackID
    return int(str(level)[-3]) - 5


def calcMaxSquare(grid):
    totalPowers = [[0 for i in range(298)] for i in range(298)]    
    
    # Calculate 3x3 total power level
    for i in range(298):
        for j in range(298):
            for k in range(i, i + 3):
                for l in range(j, j + 3):
                    totalPowers[i][j] += grid[k][l]

    # Find x, y of max total power level
    max = -100
    x = -1
    y = -1

    for i in range(298):
        for j in range(298):
            if totalPowers[i][j] > max:
                max = totalPowers[i][j]
                x = i + 1
                y = j + 1

    return x, y


if __name__ == "__main__":
    main()
