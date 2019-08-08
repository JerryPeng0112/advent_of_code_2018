import re

def main():

    state, lookup = readFiles()

    sum = calcPlantSum(state, lookup)

    print(sum)


def calcPlantSum(state, lookup):
    total = 0
    negative = 0

    # The shape converges by 98th cycle
    for i in range(98):
        newState = ''
        state, negativeAdded = addExtensions(state)
        negative -= negativeAdded

        for i in range(2, len(state) - 2):
            newState += lookup[state[i - 2:i + 3]]

        state = state[:2] + newState + state[-2:]

    for i in range(len(state)):
        if state[i] == '#':
            total += i + negative + 50000000000 - 98

    return total


def addExtensions(state):
    firstPotIdx = state.index('#')
    negativeAdded = 0
    negativeAdded = 5 - firstPotIdx

    if firstPotIdx < 5:
        state = ('.' * negativeAdded) + state
    else:
        state = state[firstPotIdx - 5:]

    lastPotIdx = state[::-1].index('#')
    if lastPotIdx < 5:
        state += '.' * (5 - lastPotIdx)

    return state, negativeAdded


def getState(line):
    pattern = re.compile(r'initial state: (.*)')
    return pattern.match(line).groups()[0]


def getComb(line):
    pattern = re.compile(r'(.*) =\> (.)')
    matches = pattern.match(line).groups()
    comb = matches[0]
    result = matches[1]
    return comb, result


def readFiles():
    # Get state
    file = open("input.txt", "r")
    state = getState(file.readline())
    file.readline()

    # Generate lookup table
    lookup = {}

    for line in file:
        comb, result = getComb(line)
        lookup[comb] = result

    file.close()
    return state, lookup


if __name__ == "__main__":
    main()
