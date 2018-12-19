def main():
    data = readFiles()

    result = calcSimilarID(data, len(data))
    print(result)

def calcSimilarID(data, dataLen):
    sortedInput = data.sort()
    idLen = len(data[0])

    for i in range(dataLen):
        diffCount = 0
        diffIdx = -1
        for j in range(idLen): 
            if data[i][j] != data[i + 1][j]:
                diffCount += 1
                diffIdx = j

        if diffCount == 1:
            return data[i][:diffIdx] + data[i][diffIdx + 1:]

def processFileLine(line):
    return line[0:-1]

def readFiles():
    data = []
    file = open("input.txt", "r")
    for line in file:
        data.append(processFileLine(line))
    return data

if __name__ == "__main__":
    main()
