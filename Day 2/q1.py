def main():
    data = readFiles()

    result = calcCheckSum(data, len(data))
    print(result)

def calcCheckSum(data, dataLen):
    twos = 0
    threes = 0

    for i in range(dataLen):
        letterCount = [0] * 26
        id = data[i]

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

def readFiles():
    data = []
    file = open("input.txt", "r")
    for line in file:
        data.append(processFileLine(line))
    file.close()
    return data

if __name__ == "__main__":
    main()
