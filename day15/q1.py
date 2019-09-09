from copy import deepcopy
from collections import deque

class Character:
    def __init__(self, x, y, charType, enemyType):
        self.hp = 10
        self.attack = 3
        self.charType = charType
        self.enemyType = enemyType
        self.x = x
        self.y = y


class Goblin(Character):
    id = 0

    def __init__(self, x, y):
        Character.__init__(self, x, y, 'goblin', 'elf')
        self.id = Goblin.id
        Goblin.id += 1


class Elf(Character):
    id = 0
    def __init__(self, x, y):
        Character.__init__(self, x, y, 'elf', 'goblin')
        self.id = Elf.id
        Elf.id += 1


def main():

    data = readFiles()

    world, chars, coorToID = scanWorld(data) 

    result = calcResult(world, chars, coorToID)

    myList = [1, 2, 3]
    myIter = filter(lambda x: x % 2 == 0, myList)
    myIter2 = map(lambda x: x * 2, myIter)


def calcResult(world, chars, coorToID):
    roundNum = 0
    inspectRounds = [1, 2, 23, 24, 25, 26, 27, 28, 47]
    printInfo(world, chars, coorToID)
    
    while bothTypeAlive(chars):


        # Merge elves and goblins into a list and sort by reading order
        elves = chars['elf']
        goblins = chars['goblin']
        charList = list(elves.values()) + list(goblins.values())
        charList.sort(key=lambda c: (c.x, c.y))

        # List for dead characters
        deadIDs = {}
        deadIDs['elf'] = []
        deadIDs['goblin'] = []

        for char in charList:

            # If character dead, skip it
            if char.id in deadIDs[char.charType]:
                continue

            # Find an adjacent target to attack
            deadID, attacked = tryAttack(world, char, chars, coorToID)

            if not attacked:

                # Find a target and move
                tryMove(world, char, chars, coorToID)

                # Find an adjacent target to attack
                deadID, attacked = tryAttack(world, char, chars, coorToID)

            # If there are enemy character dead, append it to list
            if deadID != None:
                deadIDs[char.enemyType].append(deadID)

        roundNum += 1
        if roundNum in inspectRounds:
            print("Round: ", roundNum)
            printInfo(world, chars, coorToID)
            input()

    return 0


def bothTypeAlive(chars):
    return chars['elf'] and chars['goblin']


def tryAttack(world, char, chars, coorToID):
    deadID, attacked = None, False
    
    # Get the target to attack
    target = getAdjacentTarget(world, char, chars, coorToID)

    if target != None:

        # Attack
        target.hp -= char.attack
        attacked = True

        # When target is dead
        if target.hp <= 0:
            del chars[target.charType][target.id]
            del coorToID[target.charType][(target.x, target.y)]
            deadID = target.id

    return deadID, attacked


def getAdjacentTarget(world, char, chars, coorToID):
    x, y = char.x, char.y
    enemyType = char.enemyType

    # Get available adjacent targets, return first reading order object
    # If none, return None
    targets = getAdjacentCoor(x, y)
    hasEnemy = lambda c: world[c[0]][c[1]] and c in coorToID[enemyType]
    targets = list(filter(hasEnemy, targets))

    # Choose coordinate first in reading order.
    # If no item in list, return None
    if len(targets) > 0:

        firstCoor = getFirstCoor(targets)
        targetID = coorToID[enemyType][firstCoor]
        return chars[enemyType][targetID]
    
    return None


def tryMove(world, char, chars, coorToID):

    # Construct distance grid
    distGridChar = getDistances(world, char.x, char.y, coorToID)

    # Get enemy neighboring coordinates
    enemyNeighborCoors = getEnemyNeighborCoors(world, char, chars)

    # Get closest reachable space with first reading order
    targetCoor = findClosestCoor(distGridChar, enemyNeighborCoors)

    # Construct distance grid from target
    distGridTarget = getDistances(world, *targetCoor, coorToID)

    # Get neighbor coordinates from character
    sourceNeighbors = getAdjacentCoor(char.x, char.y)

    # Get reachable space with first reading order
    moveCoor = findClosestCoor(distGridTarget, sourceNeighbors)

    # Move character
    if moveCoor:
        del coorToID[char.charType][(char.x, char.y)]
        char.x = moveCoor[0]
        char.y = moveCoor[1]
        coorToID[char.charType][(char.x, char.y)] = char.id


def findClosestCoor(distGrid, coors):

    # Lambda Functions
    # Check if the coordinate is reachable
    reachable = lambda c: distGrid[c[0]][c[1]] > -1
    # Map coordinate to distance
    coorToDist = lambda c: distGrid[c[0]][c[1]]
    # Check if distance equal minDist
    equalMinDist = lambda c: distGrid[c[0]][c[1]] == minDist

    # Get reachable coordinates, and get ones with minimum distance
    reachableCoors = list(filter(reachable, coors))
    minDist = min(map(coorToDist, reachableCoors))
    minDistCoors = list(filter(equalMinDist, reachableCoors))

    # Choose first coordinate from reading order
    chosenCoor = None
    if len(minDistCoors) > 0:
        chosenCoor = getFirstCoor(minDistCoors)

    return chosenCoor


def getDistances(world, x, y, coorToID):
    numRow = len(world)
    numCol = len(world[0])

    queue = deque()
    distGrid = [[-1 for i in range(numCol)] for i in range(numRow)]
    distGrid[x][y] = 0

    appendValidNeighbors(world, coorToID, distGrid, queue, x, y)

    while(queue):

        # Get next coordinate, calculate distance based on neighbors
        coor = queue.popleft()
        x, y = coor[0], coor[1]

        # If the coordinate distance is calculated, skip iteration
        if (distGrid[x][y] != -1):
            continue

        neighbors = getAdjacentCoor(x, y)
        appendValidNeighbors(world, coorToID, distGrid, queue, x, y)

        discovered = lambda c: distGrid[c[0]][c[1]] != -1
        coorToDist = lambda c: distGrid[c[0]][c[1]]

        discoveredCoor = filter(discovered, neighbors)
        minDist = min(map(coorToDist, discoveredCoor))
        distGrid[coor[0]][coor[1]] = minDist + 1

    return distGrid


def getEnemyNeighborCoors(world, char, chars):
    enemies = chars[char.enemyType]
    coors = set()

    for enemyID, enemy in enemies.items():

        enemyNeighbors = getAdjacentCoor(enemy.x, enemy.y)
        coors.update(enemyNeighbors)

    return list(coors)
    

def appendValidNeighbors(world, coorToID, distGrid, queue, x, y):
    # Append valid neighbors, which are not walls, occupied and
    # distances not calculated
    neighbors = getAdjacentCoor(x, y)
    valid = lambda c: world[c[0]][c[1]] == '.' and c not in coorToID['elf'] and \
            c not in coorToID['goblin'] and distGrid[c[0]][c[1]] == -1

    neighbors = filter(valid, neighbors)
    queue.extend(neighbors)


def getAdjacentCoor(x, y):
    return [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]


def getFirstCoor(targets):
    targets.sort(key=lambda x: (x[0], x[1]))
    return targets[0]


def printInfo(world, chars, coorToID):

    # Print all character infos
    print("Elves")
    for k, v in chars['elf'].items():
        print(vars(v))
    print("Goblins")
    for k, v in chars['goblin'].items():
        print(vars(v))

    # Verify coor and ID linked correctly
    if len(chars['elf']) != len(coorToID['elf']):
        print("Elf: mismatch coor ID length")
    if len(chars['goblin']) != len(coorToID['goblin']):
        print("Goblin: mismatch coor ID length")

    for charID, char in chars['elf'].items():
        if coorToID['elf'][(char.x, char.y)] != char.id:
            print('Elf: coor ID linkage problem')
    for charID, char in chars['goblin'].items():
        if coorToID['goblin'][(char.x, char.y)] != char.id:
            print('Goblin: coor ID linkage problem')

    # Print map
    worldCopy = deepcopy(world)
    symbols = {
        'goblin': 'G',
        'elf': 'E',
    }
    for charID, char in chars['elf'].items():
        worldCopy[char.x][char.y] = symbols[char.charType]
    for charID, char in chars['goblin'].items():
        worldCopy[char.x][char.y] = symbols[char.charType]

    for row in worldCopy:
        print(''.join(row))

    print()


def scanWorld(data):
    chars, elves, goblins = {}, {}, {}
    coorToID, elfCoorToID, goblinCoorToID = {}, {}, {}
    numRow = len(data)
    numCol = len(data[0])

    # Record elves, goblins coordinates
    for i in range(numRow):
        for j in range(numCol):

            if data[i][j] == 'G':
                goblin = Goblin(i, j)
                goblins[goblin.id] = goblin
                goblinCoorToID[(i, j)] = goblin.id
                data[i][j] = '.'

            if data[i][j] == 'E':
                elf = Elf(i, j)
                elves[elf.id] = elf
                elfCoorToID[(i, j)] = elf.id
                data[i][j] = '.'

    chars = {
        'elf': elves,
        'goblin': goblins,
    }

    coorToID = {
        'elf': elfCoorToID,
        'goblin': goblinCoorToID
    }

    return data, chars, coorToID


def readLine(line):
    return list(line.strip('\n'))


def readFiles():
    data = []
    file = open("test2.txt", "r")

    for line in file:
        data.append(readLine(line))

    file.close()
    return data


if __name__ == "__main__":
    main()


"""
Plan:
Read map, map all Goblins and Elves to goblins/Elves(dict: id->obj)
for sorted goblins/elves by coordinates
    Check if there are adjacent enemies to attack
    if not, move
        Create distance map, find nearest reachable target.
        From that target, create distance map, choose step.
    After move, check if there are adjacent enemies to attack
"""

"""
walls (#), space (.), Goblin (G) Elf (E)
Round: Move, Attack

If in range of attack, don't move, attack instead.

Move:
- Begin by identifying all possible targets
- Find nearest reachable target, if tied choose first in reading order
- Choose step with shortest path, if tied, choose first in reading order

Attack:
- If unites in range, fewest HP selected. If tied, choose first in reading order
- Once units die, its square becomes a space.

End:
- Combat only ends when a unit finds no targets during its turn
- Find (number of full rounds that were completed) * (sum of the HPs of remaining units at the moment combats end).
"""
