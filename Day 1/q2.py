from functools import reduce

def main():
    input = []
    readFiles(input)

    result = getRepeatedFreq(input)
    print(result)

def getRepeatedFreq(input):
    sum = 0
    visited = {}
    visited[sum] = True
    inputLen = len(input)

    while(True):
        for i in range(inputLen):
            sum += input[i]
            if sum in visited:
                return sum
            else:
                visited[sum] = True

def processFileLine(line):
    return int(line)

def readFiles(input):
    file = open("input.txt", "r")
    for line in file:
        input.append(processFileLine(line))

if __name__ == "__main__":
    main()
