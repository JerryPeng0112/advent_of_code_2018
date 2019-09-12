from collections import deque


class Room():
    def __init__(self):
        self.n = None
        self.w = None
        self.e = None
        self.s = None
        self.depth = None


def main():

    pathStr = readFiles()

    start = buildRooms(pathStr)

    maxDepth = getMaxDepth(start)

    print(maxDepth)


def getMaxDepth(start):
    
    maxDepth = 0
    start.depth = 0
    roomQueue = deque([start])

    # Get depth of all rooms
    while roomQueue:
        
        # Get current room
        curr = roomQueue.popleft()
        currDepth = curr.depth

        # If room depth not set, set adjacent rooms depth, 
        # and append the rooms to queue
        if curr.n:
            if not curr.n.depth:
                curr.n.depth = currDepth + 1
                roomQueue.append(curr.n)

        if curr.w:
            if not curr.w.depth:
                curr.w.depth = currDepth + 1
                roomQueue.append(curr.w)

        if curr.e:
            if not curr.e.depth:
                curr.e.depth = currDepth + 1
                roomQueue.append(curr.e)

        if curr.s:
            if not curr.s.depth:
                curr.s.depth = currDepth + 1
                roomQueue.append(curr.s)

        maxDepth = max(maxDepth, currDepth)

    return maxDepth


def buildRooms(pathStr):

    # Starting room
    start = Room()
    curr = start

    splitStack = deque([])

    # Loop through the path strings to build rooms
    for char in pathStr:
        
        # char is a direction character, build room and move to it
        if char == 'N':
            if not curr.n:
                curr.n = Room()
                curr.n.s = curr
            curr = curr.n

        elif char == 'W':
            if not curr.w:
                curr.w = Room()
                curr.w.e = curr
            curr = curr.w
        elif char == 'E':
            if not curr.e:
                curr.e = Room()
                curr.e.w = curr
            curr = curr.e
        elif char == 'S':
            if not curr.s:
                curr.s = Room()
                curr.s.n = curr
            curr = curr.s

        # If char is '(' signaling a split, push room to stack
        elif char == '(':
            splitStack.append(curr)

        # If char is ')' signaling closing a split
        elif char == ')':
            curr = splitStack.pop()

        # If char is '|', signaling a backtrack, retrieve top room of room stack
        elif char == '|':
            curr = splitStack[-1]
            
    return start




def readFiles():
    file = open('input.txt', 'r')
    pathStr = file.read().strip('\n')[1:-1]
    file.close()
    return pathStr


if __name__ == '__main__':
    main()
