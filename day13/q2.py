from enum import Enum


class DIRECTION(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3



class Cart:
    # Reference for turns
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
    id = 0


    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction.value
        # For intersection turns
        self.turnMem = -1

        # Increment ID
        self.id = Cart.id
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
        if symbol in Cart.refs:
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
    y, x = findLastCart(mineMap, carts)

    print('%r,%r' % (x, y))


def scanCarts(mineMap):
    carts = {}
    numRows = len(mineMap)
    numCols = len(mineMap[0])

    for i in range(numRows):
        for j in range(numCols):

            if mineMap[i][j] == '<':
                mineMap[i][j] = '-'
                cart = Cart(i, j, DIRECTION.LEFT)
                carts[cart.id] = cart

            elif mineMap[i][j] == '^':
                mineMap[i][j] = '|'
                cart = Cart(i, j, DIRECTION.UP)
                carts[cart.id] = cart

            elif mineMap[i][j] == '>':
                mineMap[i][j] = '-'
                cart = Cart(i, j, DIRECTION.RIGHT)
                carts[cart.id] = cart

            elif mineMap[i][j] == 'v':
                mineMap[i][j] = '|'
                cart = Cart(i, j, DIRECTION.DOWN)
                carts[cart.id] = cart

    return carts


def findLastCart(mineMap, carts):
    prevCoors = {}

    # Record cart coordinate in dict
    for cartID, cart in carts.items():
        prevCoors[(cart.x, cart.y)] = cartID

    # Run ticks
    while len(carts) > 1:
        removeList = set()
        coors = {}
        idToCoors = {}

        # Sort cart by coordinate
        carts = {k: carts[k] for k in sorted(carts, key=lambda c: (carts[c].x, carts[c].y))}

        for cartID, cart in carts.items():

            # Move and turn
            cart.move()

            x, y = cart.x, cart.y
            cart.turn(mineMap[x][y])

            # Check crash
            if (x, y) in coors:
                removeList.add(coors[(x,y)])
                removeList.add(cartID)

            elif (x, y) in prevCoors:
                removeList.add(prevCoors[(x, y)])
                removeList.add(cartID)


            # Update coordinate record
            coors[(x, y)] = cartID
            idToCoors[cartID] = (x, y)

        # Useful info printing
        #print(prevCoors)
        #print(coors)
        #print(idToCoors)
        #printMap(mineMap, coors, carts)

        # remove carts
        removeCarts(carts, removeList, coors, idToCoors)

        # Copy current coordinates to prevCoors for next tick
        prevCoors = dict(coors)

    lastCart = list(carts.values())[0]
    return lastCart.x, lastCart.y


def removeCarts(carts, removeList, coors, idToCoors):
    coors = {coor: cartID for coor, cartID in coors.items() if cartID not in removeList}

    for cartID in removeList:
        del carts[cartID]
        del idToCoors[cartID]



def printMap(mineMap, coors, carts):
    numRows = len(mineMap)
    numCols = len(mineMap[0])

    for i in range(numRows):
        string = ""

        for j in range(numCols):
            char = mineMap[i][j]

            if (i, j) in coors:
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
