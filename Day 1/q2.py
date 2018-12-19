def main():

    data = readFiles()

    result = getRepeatedFreq(data)
    print(result)

def getRepeatedFreq(data):
    sum = 0
    visited = {}
    visited[sum] = True
    dataLen = len(data)

    while(True):
        for i in range(dataLen):
            sum += data[i]
            if sum in visited:
                return sum
            else:
                visited[sum] = True

def processFileLine(line):
    return int(line)

def readFiles():
    data = []
    file = open("input.txt", "r")
    for line in file:
        data.append(processFileLine(line))
    return data

if __name__ == "__main__":
    main()
