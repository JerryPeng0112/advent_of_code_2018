from enum import Enum

class DIRECTION(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


class Cart:
    # Reference for turns
    id = 0
    refs = {
        '/': {
            DIRECTION.LEFT.value: -1,
            DIRECTION.UP.value: 1, 
            DIRECTION.RIGHT.value: -1,
            DIRECTION.DOWN.value: 1,
        },
        '\\': {
            DIRECTION.LEFT.value: 1,
            DIRECTION.UP.value: -1,
            DIRECTION.RIGHT.value: 1,
            DIRECTION.DOWN.value: -1,
        }
    }


    def __init__(self, x, y, direction):
        self.id = Cart.id
        self.x = x
        self.y = y
        self.direction = direction.value
        # For intersection turns
        self.turnMem = -1

        # Increment ID
        Cart.id += 1

    
    def move(self):
        if self.direction == DIRECTION.LEFT.value:
            self.y -= 1
        elif self.direction == DIRECTION.UP.value:
            self.x -= 1
        elif self.direction == DIRECTION.RIGHT.value:
            self.y += 1
        else:
            self.x += 1


    def turn(self, symbol):
        if symbol in Cart.refs.keys():
            self.changeDir(Cart.refs[symbol][self.direction])

        elif symbol == '+':
            self.changeDir(self.turnMem)
            self.turnMem = (self.turnMem + 2) % 3 - 1

    
    def changeDir(self, turnDir):
        self.direction += turnDir

        if self.direction == -1:
            self.direction = 3

        elif self.direction == 4:
            self.direction = 0



def main():

    mineMap = readFiles()

    carts = scanCarts(mineMap)

    # Reverse x, y due to inverted axis
    y, x = findCrash(mineMap, carts)

    print('%r,%r' % (x, y))


def scanCarts(mineMap):
    carts = []
    numRows = len(mineMap)
    numCols = len(mineMap[0])

    for i in range(numRows):
        for j in range(numCols):

            if mineMap[i][j] == '<':
                mineMap[i][j] = '-'
                cart = Cart(i, j, DIRECTION.LEFT)
                carts.append(cart)

            elif mineMap[i][j] == '^':
                mineMap[i][j] = '|'
                cart = Cart(i, j, DIRECTION.UP)
                carts.append(cart)

            elif mineMap[i][j] == '>':
                mineMap[i][j] = '-'
                cart = Cart(i, j, DIRECTION.RIGHT)
                carts.append(cart)

            elif mineMap[i][j] == 'v':
                mineMap[i][j] = '|'
                cart = Cart(i, j, DIRECTION.DOWN)
                carts.append(cart)

    return carts


def findCrash(mineMap, carts):
    prevCoors = {}
    numCarts = len(carts)

    # Record cart coordinate in dict
    for i in range(numCarts):
        cart = carts[i]
        prevCoors[(cart.x, cart.y)] = i

    # Run steps
    while True:
        coors = {}
        idToCoors = {}

        # Sort cart by coordinate
        carts.sort(key=lambda c: (c.x, c.y))

        for i in range(numCarts):
            cart = carts[i]
            x, y = cart.x, cart.y

            # Move and turn
            cart.move()

            x, y = cart.x, cart.y
            cart.turn(mineMap[x][y])

            # Check crash during tick
            if (x, y) in coors.keys():
                return x, y

            if (x, y) in prevCoors.keys():
                return x, y

            # Update coordinate record
            cartID = cart.id
            coors[(x, y)] = cartID
            idToCoors[cartID] = (x, y)

        # Useful info printing
        #print(prevCoors)
        #print(coors)
        #print(idToCoors)
        #printMap(mineMap, coors, carts)

        # Copy current coordinates to prevCoors for next tick
        prevCoors = dict(coors)


def printMap(mineMap, coors, carts):
    numRows = len(mineMap)
    numCols = len(mineMap[0])

    for i in range(numRows):
        string = ""

        for j in range(numCols):
            char = mineMap[i][j]

            if (i, j) in coors.keys():
                direction = carts[coors[(i, j)]].direction

                if direction == DIRECTION.LEFT.value:
                    char = '<'
                elif direction == DIRECTION.UP.value:
                    char = '^'
                elif direction == DIRECTION.RIGHT.value:
                    char = '>'
                elif direction == DIRECTION.DOWN.value:
                    char = 'v'

            string += char

        print(string)

    print()


def readFiles():
    mineMap = []
    file = open("input.txt", "r")

    for line in file:
        mineMap.append(list(line.rstrip('\n')))

    file.close()
    return mineMap


if __name__ == "__main__":
    main()
