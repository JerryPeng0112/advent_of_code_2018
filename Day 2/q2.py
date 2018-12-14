from functools import reduce

def main():
    inputs = []
    readFiles(inputs)

    result = calcSimilarID(inputs, len(inputs))
    print(result)

def calcSimilarID(inputs, inputsLen):
    sortedInput = inputs.sort()
    idLen = len(inputs[0])

    for i in range(inputsLen):
        diffCount = 0
        diffIdx = -1
        for j in range(idLen): 
            if inputs[i][j] != inputs[i + 1][j]:
                diffCount += 1
                diffIdx = j

        if diffCount == 1:
            return inputs[i][:diffIdx] + inputs[i][diffIdx + 1:]

def processFileLine(line):
    return line[0:-1]

def readFiles(inputs):
    file = open("input.txt", "r")
    for line in file:
        inputs.append(processFileLine(line))

if __name__ == "__main__":
    main()
