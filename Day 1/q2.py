from functools import reduce

def main():
    inputs = []
    readFiles(inputs)

    result = getRepeatedFreq(inputs)
    print(result)

def getRepeatedFreq(inputs):
    sum = 0
    visited = {}
    visited[sum] = True
    inputsLen = len(inputs)

    while(True):
        for i in range(inputsLen):
            sum += inputs[i]
            if sum in visited:
                return sum
            else:
                visited[sum] = True

def processFileLine(line):
    return int(line)

def readFiles(inputs):
    file = open("input.txt", "r")
    for line in file:
        inputs.append(processFileLine(line))

if __name__ == "__main__":
    main()
