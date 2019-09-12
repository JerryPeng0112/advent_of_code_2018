from collections import deque
import re


def main():

    fileData = readFiles()

    ipReg, program = parseProgram(fileData)

    #reg = runProgram(ipReg, program)

    r4 = runOptimizedProgram(program[7]['A'])
    
    print(r4)


def runOptimizedProgram(num):
    r4 = 0
    r4Mem = set()
    lastR4 = -1

    while True:
        r3 = r4 | 65536
        r4 = num

        while True:

            r4 = ((((r3 & 255) + r4) & 16777215) * 65899) & 16777215
            
            if r3 < 256:

                # If r4 not found, add it to set
                if r4 not in r4Mem:
                    r4Mem.add(r4)
                    lastR4 = r4
                    break

                # If repeated r4 found, output last r4
                else:
                    return lastR4

            # Optimized from test program line 18-26
            r3 = r3 // 256


def parseProgram(fileData):
    ipData = fileData[0]
    programData = fileData[1:]

    # Get instruction pointer register
    ipPattern = re.compile(r'\#ip (\d)')
    ipReg = ipPattern.match(ipData).groups()[0]
    ipReg = int(ipReg)

    # Parse program
    program = list(map(lambda d: toInstrType(d), programData))

    return ipReg, program


def toInstrType(d):
    # Convert instruction text to instruction data structure
    instruction = d.split(' ')
    instruction = {
        'op': instruction[0],
        'A': int(instruction[1]),
        'B': int(instruction[2]),
        'C': int(instruction[3]),
    }

    return instruction


"""
Instruction operation functions
"""

def addr(reg, instr):
    reg[instr['C']] = reg[instr['A']] + reg[instr['B']]
    return reg


def addi(reg, instr):
    reg[instr['C']] = reg[instr['A']] + instr['B']
    return reg


def mulr(reg, instr):
    reg[instr['C']] = reg[instr['A']] * reg[instr['B']]
    return reg
    

def muli(reg, instr):
    reg[instr['C']] = reg[instr['A']] * instr['B']
    return reg


def banr(reg, instr):
    reg[instr['C']] = reg[instr['A']] & reg[instr['B']]
    return reg
    

def bani(reg, instr):
    reg[instr['C']] = reg[instr['A']] & instr['B']
    return reg


def borr(reg, instr):
    reg[instr['C']] = reg[instr['A']] | reg[instr['B']]
    return reg
    

def bori(reg, instr):
    reg[instr['C']] = reg[instr['A']] | instr['B']
    return reg


def setr(reg, instr):
    reg[instr['C']] = reg[instr['A']]
    return reg
    

def seti(reg, instr):
    reg[instr['C']] = instr['A']
    return reg


def gtir(reg, instr):
    reg[instr['C']] = 1 if instr['A'] > reg[instr['B']] else 0
    return reg


def gtri(reg, instr):
    reg[instr['C']] = 1 if reg[instr['A']] > instr['B'] else 0
    return reg


def gtrr(reg, instr):
    reg[instr['C']] = 1 if reg[instr['A']] > reg[instr['B']] else 0
    return reg


def eqir(reg, instr):
    reg[instr['C']] = 1 if instr['A'] == reg[instr['B']] else 0
    return reg


def eqri(reg, instr):
    reg[instr['C']] = 1 if reg[instr['A']] == instr['B'] else 0
    return reg


def eqrr(reg, instr):
    reg[instr['C']] = 1 if reg[instr['A']] == reg[instr['B']] else 0
    return reg


def readFiles():
    data = []
    file = open('input.txt', 'r')
    data = file.read().split('\n')[:-1]
    file.close()
    return data


if __name__ == '__main__':
    main()
