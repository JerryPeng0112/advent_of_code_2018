def main():

    input = readFiles()

    print(input)


def readLine(line):
    return line


def readFiles():
    data = []
    file = open("input.txt", "r")

    for line in file:
        data.append(readLine(line))

    file.close()
    return data


if __name__ == "__main__":
    main()
