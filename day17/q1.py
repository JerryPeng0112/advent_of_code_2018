from PIL import Image
from collections import deque
import re


def main():

    data = readFiles()

    world, start, minY = constructWorld(data)

    world = runWater(world, start)
    printWorldImage(world)

    numWaterSpaces = countWaterSpaces(world, minY)

    print(numWaterSpaces)


def countWaterSpaces(world, minY):
    # Count spaces that have water symbols '|', '~'
    countSymbols = lambda d: len(list(filter(lambda x: x in ['|', '~'], d)))
    rowCounts = list(map(lambda d: countSymbols(d), world[minY:]))
    return sum(rowCounts)


def runWater(world, start):
    
    # Queue for flowing water starting points
    flowQueue = deque([start])

    # Set for recording Water flow starting points
    flows = set()

    # Loop til all water flow ends
    while flowQueue:
        
        # Get start of water flow
        flowStart = flowQueue.popleft()
        dropQueue = deque([])

        # Water drops
        dropSpace = list(flowStart)
        flowOut = drop(world, dropQueue, dropSpace)

        # If flows out, do not flow left and right
        if flowOut:
            continue

        while dropQueue:

            # Get drop space, start of flow
            dropSpace = dropQueue.pop()

            newFlows = fill(world, dropSpace, flows)

            # If there are new flows, add them to queue, as well as the flowstart
            # To ensure tanks are filled completely
            if newFlows:
                flowQueue.extend(newFlows)
                flowQueue.append(flowStart)
                break
                    
    return world



def drop(world, dropQueue, dropSpace):

    while True:

        dropSpace[1] += 1

        # If drop out of bound
        if dropSpace[1] > len(world) - 1:
            return True

        # If wall or filled water, stop dropping
        elif getSpace(world, dropSpace) in ['#', '~']:
            return False

        else:
            setSpace(world, dropSpace, '|')
            dropQueue.append(list(dropSpace))


def fill(world, dropSpace, flows):

    newFlows = []
    xLeft, xRight = None, None

    # Flow left
    flowSpace = list(dropSpace)
    while(True):

        belowSpace = list(flowSpace)
        belowSpace[1] += 1

        # Check if current space is wall
        if getSpace(world, flowSpace) == '#':
            xLeft = flowSpace[0] + 1
            break

        # Check space below is not a wall or water
        if getSpace(world, belowSpace) not in ('~', '#'):

            # Check if new flow is added prior
            if tuple(flowSpace) not in flows:
                flows.add(tuple(flowSpace))
                setSpace(world, flowSpace, '|')
                newFlows.append(flowSpace)
            break

        setSpace(world, flowSpace, '|')
        flowSpace[0] -= 1

    # Flow right
    flowSpace = list(dropSpace)
    while(True):

        belowSpace = list(flowSpace)
        belowSpace[1] += 1

        # Check if current space is wall
        if getSpace(world, flowSpace) == '#':
            xRight = flowSpace[0] - 1
            break

        # Check space below is not a wall or water
        if getSpace(world, belowSpace) not in ('~', '#'):

            # Check if new flow is added prior
            if tuple(flowSpace) not in flows:
                flows.add(tuple(flowSpace))
                newFlows.append(flowSpace)
                setSpace(world, flowSpace, '|')
            break

        setSpace(world, flowSpace, '|')
        flowSpace[0] += 1

    # If the flow fill tank, set space to '~'
    if xLeft and xRight:
        for i in range(xLeft, xRight + 1):
            setSpace(world, [i, flowSpace[1]], '~')

    return newFlows


def getSpace(world, dropSpace):
    # Return the character in world space
    return world[dropSpace[1]][dropSpace[0]]


def setSpace(world, dropSpace, char):
    # Set the world space to character
    world[dropSpace[1]][dropSpace[0]] = char


def constructWorld(data):
    # Translate x coordinate from x minimum to 0
    minX = min(map(lambda d: d['x1'], data)) - 1
    maxX = max(map(lambda d: d['x2'], data)) + 2
    minY = min(map(lambda d: d['y1'], data))
    maxY = max(map(lambda d: d['y2'], data)) + 1

    for d in data:
        d['x1'] -= minX
        d['x2'] -= minX

    # Create world
    world = [['.' for i in range(maxX - minX)] for i in range(maxY)]

    # Add walls
    for d in data:
        for x in range(d['x1'], d['x2'] + 1):
            for y in range(d['y1'], d['y2'] + 1):
                world[y][x] = '#'

    # Add starting water flow
    start = [500 - minX, 0]
    world[start[1]][start[0]] = '+'


    return world, start, minY


def printWorld(world):
    maxY = len(world)

    for y in range(maxY):
        print(''.join(world[y]))

    print()


def printWorldImage(world):
    numY = len(world)
    numX = len(world[0])

    img = Image.new( 'RGB', (numX, numY), "white")
    pixels = img.load()

    for y in range(numY):
        for x in range(numX):

            if world[y][x] == '#':
                pixels[x,y] = (0, 0, 0)
            elif world[y][x] == '~':
                pixels[x,y] = (0, 0, 255)
            elif world[y][x] == '|':
                pixels[x,y] = (0, 128, 128)



    img.show()



def readLine(line):
    yRangeMatcher = re.compile(r'^x=(\d+), y=(\d+)..(\d+)$')
    xRangeMatcher = re.compile(r'^y=(\d+), x=(\d+)..(\d+)$')

    coors = {}
    if line[0] == 'x':
        values = yRangeMatcher.match(line).groups()
        coors['x1'] = int(values[0])
        coors['x2'] = int(values[0])
        coors['y1'] = int(values[1])
        coors['y2'] = int(values[2])
    else:
        values = xRangeMatcher.match(line).groups()
        coors['y1'] = int(values[0])
        coors['y2'] = int(values[0])
        coors['x1'] = int(values[1])
        coors['x2'] = int(values[2])

    return coors


def readFiles():
    data = []
    file = open('input.txt', 'r')

    for line in file:
        data.append(readLine(line))

    file.close()
    return data


if __name__ == '__main__':
    main()
