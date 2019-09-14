import re
import math
from heapq import heappush, heappop
from datetime import datetime


class HeapNode:
    def __init__(self, node, priority):
        self.node = node
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority


def main():

    fileStr = readFiles()

    depth, target = getData(fileStr)

    grid = buildGrid(depth, target)

    #printGrid(grid, target)

    nodes, edges = buildGraph(grid)

    cost = dijkstra(nodes, edges, (0, 0, 'torch'), (target[0], target[1], 'torch'))

    print(cost)


def dijkstra(nodes, edges, start, target):

    q = [HeapNode(start, 0)]
    visited = set()
    nodes[start] = 0
    curr = start

    nodeLen = len(nodes)

    while curr != target:

        dist = nodes[curr]
        for edge in edges[curr]:
            if nodes[edge] > nodes[curr] + edges[curr][edge]:
                nodes[edge] = nodes[curr] + edges[curr][edge]
                heappush(q, HeapNode(edge, nodes[edge]))

        visited.add(curr)

        curr = heappop(q).node
        while curr in visited:
            curr = heappop(q).node

    return nodes[target]


def buildGraph(grid):

    maxX = len(grid)
    maxY = len(grid[0])
    nodes = {}
    edges = {}
    
    validItems = [['gear', 'torch'], ['gear', 'none'], ['torch', 'none']]
    
    # Construct nodes
    for i in range(maxX):
        for j in range(maxY):

            for item in validItems[grid[i][j]]:
                nodes[(i, j, item)] = math.inf
                edges[(i, j, item)] = {}

    # Connect edges
    for i in range(maxX):
        for j in range(maxY):

            items = validItems[grid[i][j]]
            # Switch items
            edges[(i, j, items[0])][(i, j, items[1])] = 7
            edges[(i, j, items[1])][(i, j, items[0])] = 7

            # Connect to neighbor nodes
            adjacentOffset = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for (offsetX, offsetY) in adjacentOffset:

                x, y = i + offsetX, j + offsetY

                if 0 <= x < maxX and 0 <= y < maxY:
                    sameItems = list(set(validItems[grid[i][j]]) & \
                            set(validItems[grid[x][y]]))
                    
                    for item in sameItems:
                        edges[(i, j, item)][(x, y, item)] = 1

    return nodes, edges


def connect(graph, node1, node2, weight):
    t = (weight, ) + node2
    heappush(graph[node1].edges, t)

def buildGrid(depth, target):
    extendX = 0 
    extendY = 13
    targetX = target[0] + extendX
    targetY = target[1] + extendY
    mod = 20183

    grid = [[0 for i in range(targetY + 1)] for i in range(targetX + 1)]

    # Calculate the grid after applying depth and erosion level modulo
    # Optimized so that actual large number multiplications do not take place
    for i in range(targetX + 1):
        for j in range(targetY + 1):
                
            indexVal = 0
            if (i == 0 and j == 0) or (i == target[0] and j == target[1]):
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


def printGrid(grid, target):
    for i, row in enumerate(grid):
        str = ''
        for j, num in enumerate(row):
            if i == target[0] and j == target[1]:
                str += 'T'
            elif num == 0:
                str += '.'
            elif num == 1:
                str += '='
            else:
                str += '|'

        print(str)


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
