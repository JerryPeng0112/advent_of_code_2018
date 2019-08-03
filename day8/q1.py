def main():

    data = readFiles()

    index, count = countEntries(data)
    print(count)


def countEntries(data, index=0):
    count = 0
    numNodes = data[index]
    numEntries = data[index + 1]
    index += 2

    for i in range(numNodes):
        index, nodeCount = countEntries(data, index)
        count += nodeCount

    for i in range(numEntries):
        count += data[index]
        index += 1

    return index, count


def readLine(line):
    return list(map(int, line.split()))


def readFiles():
    data = None
    file = open("input.txt", "r")

    for line in file:
        data = readLine(line)

    file.close()
    return data


if __name__ == "__main__":
    main()
