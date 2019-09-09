from copy import deepcopy
from collections import deque

class Character:
    def __init__(self, x, y, charType, enemyType):
        self.hp = 200
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

    roundNum = calcRound(world, chars, coorToID)

    outcome = calcOutCome(roundNum, chars)


def calcRound(world, chars, coorToID):

    roundNum = 0
    inspectRounds = []
    print("Initial state")
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

        # Check if full round passed
        isFullRound = True

        for char in charList:

            if not bothTypeAlive(chars):
                isFullRound = False

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

        if isFullRound:
            roundNum += 1

            # Print rounds using inspect round
            if roundNum in inspectRounds:
                print("Round: ", roundNum)
                printInfo(world, chars, coorToID)

    print("Round: ", roundNum)
    printInfo(world, chars, coorToID)

    return roundNum


def bothTypeAlive(chars):
    return chars['elf'] and chars['goblin']


def tryAttack(world, char, chars, coorToID):
    deadID, attacked = None, False
    
    # Get the target to attack
    enemy = getAdjacentTarget(world, char, chars, coorToID)

    if enemy != None:

        # Attack
        enemy.hp -= char.attack
        attacked = True

        # When target is dead
        if enemy.hp <= 0:
            del chars[enemy.charType][enemy.id]
            del coorToID[enemy.charType][(enemy.x, enemy.y)]
            deadID = enemy.id

    return deadID, attacked


def getAdjacentTarget(world, char, chars, coorToID):
    x, y = char.x, char.y
    enemyType = char.enemyType

    # Get available adjacent targets, return first reading order object
    # If none, return None
    adjacentCoors = getAdjacentCoor(x, y)
    hasEnemy = lambda c: world[c[0]][c[1]] and c in coorToID[enemyType]
    enemyCoors = list(filter(hasEnemy, adjacentCoors))

    # If no item in list, return None
    if len(enemyCoors) > 0:

        # Choose lowest hp enemy
        enemyIDs = map(lambda c: coorToID[enemyType][c], enemyCoors)
        minHP = min(map(lambda charID: chars[enemyType][charID].hp, enemyIDs))
        hpEqualMinHP = lambda c: chars[enemyType][coorToID[enemyType][c]].hp == minHP
        enemyCoorsMinHP = list(filter(hpEqualMinHP, enemyCoors))

        # Choose first in reading order.
        firstCoor = getFirstCoor(enemyCoorsMinHP)
        enemyID = coorToID[enemyType][firstCoor]
        return chars[enemyType][enemyID]
    
    return None


def tryMove(world, char, chars, coorToID):

    # Construct distance grid
    distGridChar = getDistances(world, char.x, char.y, coorToID)

    # Get enemy neighboring coordinates
    enemyNeighborCoors = getEnemyNeighborCoors(world, char, chars)

    # Get closest reachable space with first reading order
    targetCoor = findClosestCoor(distGridChar, enemyNeighborCoors)

    if not targetCoor:
        return

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

    # Get reachable coordinates
    reachableCoors = list(filter(reachable, coors))

    # If no reachable coordinate found, return None
    if not reachableCoors:
        return None

    # Get coordinates with minimum distances
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


def calcOutCome(roundNum, chars):

    charsWon = None
    if chars['elf']:
        charsWon = chars['elf']
    elif chars['goblin']:
        charsWon = chars['goblin']

    totalHP = sum(map(lambda c: c.hp, list(charsWon.values())))

    print(roundNum, '*', totalHP, '=', roundNum * totalHP)

    return roundNum * totalHP


def getAdjacentCoor(x, y):
    return [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]


def getFirstCoor(targets):
    targets.sort(key=lambda x: (x[0], x[1]))
    return targets[0]


def printInfo(world, chars, coorToID):

    # Sort and Print all character infos
    elves = list(chars['elf'].values())
    goblins = list(chars['goblin'].values())
    elves.sort(key=lambda c: (c.x, c.y))
    goblins.sort(key=lambda c: (c.x, c.y))

    print("Elves")
    for elf in elves:
        print(vars(elf))
    print("Goblins")
    for goblin in goblins:
        print(vars(goblin))

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
    file = open("test4.txt", "r")

    for line in file:
        data.append(readLine(line))

    file.close()
    return data


if __name__ == "__main__":
    main()
