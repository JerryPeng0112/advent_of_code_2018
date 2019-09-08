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


def calcResult(world, chars, coorToID):

    printChars(chars, coorToID)
    
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
                move(world, char, chars, coorToID)

                # Find an adjacent target to attack
                deadID, attacked = tryAttack(world, char, chars, coorToID)

            # If there are enemy character dead, append it to list
            if deadID != None:
                deadIDs[char.enemyType].append(deadID)

        printChars(chars, coorToID)



def bothTypeAlive(chars):
    return chars['elf'] and chars['goblin']


def tryAttack(world, char, chars, coorToID):

    deadID, attacked = None, False
    
    # Get the target to attack
    target = getAdjacentTarget(world, char, chars, coorToID)

    if target != None:

        target.hp -= char.attack
        attacked = True

        if target.hp <= 0:
            del chars[target.charType][target.id]
            del coorToID[target.charType][(target.x, target.y)]
            deadID = target.id

    return deadID, attacked


def getAdjacentTarget(world, char, chars, coorToID):

    x = char.x
    y = char.y
    enemyType = char.enemyType

    targets = [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]
    targets = filter(lambda x: world[x[0]][x[1]] == '.', targets)
    targets = list(filter(lambda x: x in coorToID[enemyType], targets))

    firstCoor = getFirstCoor(targets)

    if firstCoor != None:
        targetID = coorToID[enemyType][firstCoor]
        return chars[enemyType][targetID]
    
    return None


def move(world, char, chars, coorToID):
    pass


def getFirstCoor(targets):
    if len(targets) > 0:
        targets.sort(key=lambda x: (x[0], x[1]))
        return targets[0]
    return None


def printChars(chars, coorToID):
    for k, v in chars['elf'].items():
        print(vars(v))
    for k, v in chars['goblin'].items():
        print(vars(v))
    for k, v in coorToID['elf'].items():
        print(k, v)
    for k, v in coorToID['goblin'].items():
        print(k, v)


def scanWorld(data):

    chars, elves, goblins = {}, {}, {}
    coorToID, elfCoorToID, goblinCoorToID = {}, {}, {}
    numRow = len(data)
    numCol = len(data[0])

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
