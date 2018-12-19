from functools import reduce

def main():
    data = readFiles()

    result = reduce(lambda x, y: x + y, data)
    print(result)

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
