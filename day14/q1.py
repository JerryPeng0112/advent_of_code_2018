def main():
    numRecipe = 110201

    score = calcScore(numRecipe)

    print(score)


def calcScore(numRecipe):
    recipes = [3, 7]
    cursor1 = 0
    cursor2 = 1
    while(len(recipes) - 10 < numRecipe):
        recipes += map(int, list(str(recipes[cursor1] + recipes[cursor2])))
        cursor1 = nextRecipe(recipes, cursor1)
        cursor2 = nextRecipe(recipes, cursor2)

    return ''.join(list(map(lambda x: chr(x + ord('0')),\
            recipes[numRecipe: numRecipe + 10])))


def nextRecipe(recipes, cursor):
    cursor += recipes[cursor] + 1
    cursor %= len(recipes)
    return cursor


if __name__ == "__main__":
    main()
