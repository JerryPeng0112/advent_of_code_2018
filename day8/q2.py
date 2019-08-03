def main():

    data = readFiles()

    index, count = countNodeValue(data)
    print(count)


def countNodeValue(data, index=0):
    count = 0
    nodeVals = []
    numNodes = data[index]
    numEntries = data[index + 1]
    index += 2

    # If no nodes, add entry values
    if numNodes == 0:
        for i in range(numEntries):
            count += data[index]
            index += 1

    else:
        # Get the child node values
        for i in range(numNodes):
            index, val = countNodeValue(data, index)
            nodeVals.append(val)

        # Add child node values to total using entries as index
        for i in range(numEntries):
            if data[index] <= len(nodeVals):
                count += nodeVals[data[index] - 1]

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
