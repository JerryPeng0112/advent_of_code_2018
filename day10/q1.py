import numpy as np
import matplotlib.pyplot as plt
import re
from copy import deepcopy


ITER = 10136


def main():

    data = readFiles()

    pos, vel = formatData(data)

    print(ITER)
    posTransformed = transform(pos, vel, ITER)
    plot(posTransformed)


def formatData(data):
    pos = list(map(lambda d: { 'x': int(d['xPos']), 'y': int(d['yPos']) }, data))
    vel = list(map(lambda d: { 'x': int(d['xVel']), 'y': int(d['yVel']) }, data))
    return pos, vel


def transform(pos, vel, i):
    posTransformed = deepcopy(pos)
    
    for j in range(len(pos)):
        posTransformed[j]['x'] += i * vel[j]['x']
        posTransformed[j]['y'] += i * vel[j]['y']

    return posTransformed


def plot(pos):
    x = np.array(list(map(lambda d: d['x'], pos)))
    y = np.array(list(map(lambda d: d['y'], pos)))

    plt.scatter(x, y)
    plt.gca().invert_yaxis()
    plt.show()


def readLine(line):
    pattern = re.compile(r'position=\<(?P<xPos>-?\d+),(?P<yPos>-?\d+)\>velocity=\<(?P<xVel>-?\d+),(?P<yVel>-?\d+)\>')

    return pattern.match(line.replace(' ', '')).groupdict()


def readFiles():
    data = []
    file = open("input.txt", "r")

    for line in file:
        data.append(readLine(line))

    file.close()
    return data


if __name__ == "__main__":
    main()
