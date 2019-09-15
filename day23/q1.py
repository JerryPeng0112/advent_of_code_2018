import re


def main():

    positions, radius = readFiles()

    numRobots = getNumRobots(positions, radius)

    print(numRobots)


def getNumRobots(positions, radius):
    
    # Find the position, radius pair of max radius robot
    maxRadius = max(radius)
    idx = radius.index(maxRadius)
    maxPos = positions[idx]

    inRange = filter(lambda d: dist(d, maxPos) <= maxRadius, positions)

    return len(list(inRange))


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


def readLine(line):
    pattern = re.compile(r'pos=<(.*),(.*),(.*)>, r=(.*)')
    g = pattern.match(line).groups()

    pos = (int(g[0]), int(g[1]), int(g[2]))
    r = int(g[3])

    return pos, r


def readFiles():
    positions = []
    radius = []
    file = open('input.txt', 'r')

    for line in file:
        pos, r = readLine(line)
        positions.append(pos)
        radius.append(r)


    file.close()
    return positions, radius


if __name__ == '__main__':
    main()
