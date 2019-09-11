from copy import deepcopy


NUM_MINUTES = 10


def main():

    land = readFiles()

    print('Initial:')
    printLand(land)

    land = runSims(land)

    print('Final:')
    printLand(land)

    resourceVal = calcResourceVal(land)
    print(resourceVal)


def calcResourceVal(land):
    numWoods = countType(land, '|')
    numLumberyards = countType(land, '#')
    return numWoods * numLumberyards


def countType(land, char):
    countChar = lambda r: len(list(filter(lambda c: c == char, r)))
    counts = list(map(lambda r: countChar(r), land))
    return sum(counts)


def runSims(land):

    numRows = len(land)
    numCols = len(land[0])

    # Run simulation
    for minute in range(NUM_MINUTES):
        newLand = deepcopy(land)

        # Run a round (minute) of simulation by looping each space
        for r in range(numRows):
            for c in range(numCols):

                # Get the land type and neighboring land types
                landType = land[r][c]
                neighborTypes = getNeighborTypes(land, r, c)

                # Change land type depending on neighboring land types
                if landType == '.':
                    if len([d for d in neighborTypes if d == '|']) >= 3:
                        newLand[r][c] = '|'

                elif landType == '|':
                    if len([d for d in neighborTypes if d == '#']) >= 3:
                        newLand[r][c] = '#'
                    
                else:
                    if '|' not in neighborTypes or '#' not in neighborTypes:
                        newLand[r][c] = '.'

        # Copy over the result from a round (minute) of simulation
        land = newLand

    return land


def getNeighborTypes(land, row, col):
    
    numRows = len(land)
    numCols = len(land[0])
    neighborTypes = []

    # Get neighbor types if coordinates exist on board
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):

            # Make sure the original land space is not counted
            if r == row and c == col:
                continue
            # Check if coordinate exist on board
            if r >= 0 and r < numRows and c >= 0 and c < numCols:
                neighborTypes.append(land[r][c])

    return neighborTypes

    
def printLand(land):
    for row in land:
        print(''.join(row))

    print()


def readLine(line):
    return list(line.strip('\n'))


def readFiles():
    data = []
    file = open('input.txt', 'r')

    for line in file:
        data.append(readLine(line))

    file.close()
    return data


if __name__ == '__main__':
    main()
