from functools import reduce

def main():
    inputs = []
    readFiles(inputs)

    result = calcCheckSum(inputs, len(inputs))
    print(result)

def calcCheckSum(inputs, inputsLen):
    twos = 0
    threes = 0

    for i in range(inputsLen):
        letterCount = [0] * 26
        id = inputs[i]

        # Find letter frequency
        for i in id:
            letterCount[letterIndex(i)] += 1

        for i in letterCount:
            if i == 2:
                twos += 1
                break

        for i in letterCount:
            if i == 3:
                threes += 1
                break

    return twos * threes

def letterIndex(letter):
    return ord(letter) - ord("a")

def processFileLine(line):
    return line[0:-1]

def readFiles(inputs):
    file = open("input.txt", "r")
    for line in file:
        inputs.append(processFileLine(line))

if __name__ == "__main__":
    main()
