import re
from collections import deque


def main():

    points = readFiles()

    numCons= getNumCons(points)

    print(numCons)


def getNumCons(points):
    
    count = 0
    while(points):

        formCons(points)
        count += 1

    return count


def formCons(points):

    start = points.pop()
    queue = deque([start])

    while(queue):

        cons = []
        curr = queue.popleft()

        for p in points:
            if dist(curr, p) <= 3:
                cons.append(p)

        for p in cons:
            points.remove(p)
            queue.append(p)



def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2]) + \
            abs(p1[3] - p2[3])



def readLine(line):
    pattern = re.compile(r'(.*),(.*),(.*),(.*)')
    g = pattern.match(line).groups()
    return (int(g[0]), int(g[1]), int(g[2]), int(g[3]))


def readFiles():
    data = set()
    file = open('input.txt', 'r')

    for line in file:
        data.add(readLine(line))

    file.close()
    return data


if __name__ == '__main__':
    main()
