import sys
sys.setrecursionlimit(100000)
def main():

    string = readFiles()

    result = reducePolymer(string)

    print(len(result))

def reducePolymer(string):
    idx = 0
    while idx != len(string) - 1:
        if canReact(string[idx], string[idx + 1]):
            string = string[:idx] + string[idx + 2:]  
            if idx != 0:
                idx -= 1
        else:
            idx += 1
    return string

def canReact(char1, char2):
    if char1.islower():
        if char2 == char1.upper():
            return True
        else:
            return False
    else:
        if char2 == char1.lower():
            return True
        else:
            return False

def readFiles():
    file = open("input.txt", "r")
    data = file.readline().strip()
    return data

if __name__ == "__main__":
    main()
