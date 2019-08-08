import re

def main():

    state, lookup = readFiles()

    sum = calcPlantSum(state, lookup)

    print(sum)


def calcPlantSum(state, lookup):
    total = 0
    negative = 0
    for i in range(20):
        newState = ''
        state, negativeAdded = addExtensions(state)
        negative -= negativeAdded

        for i in range(2, len(state) - 2):
            newState += lookup[state[i - 2:i + 3]]

        state = state[:2] + newState + state[-2:]

    for i in range(len(state)):
        if state[i] == '#':
            total += i + negative

    return total


def addExtensions(state):
    firstPotIdx = state.index('#')
    negativeAdded = 0

    if firstPotIdx < 5:
        negativeAdded = 5 - firstPotIdx
        state = ('.' * negativeAdded) + state

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
