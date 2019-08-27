def main():
    score = 110201

    numRecipes = matchScore(str(score))

    print(numRecipes)


def matchScore(score):
    recipes = [3, 7]
    cursor1 = 0
    cursor2 = 1

    matched = False

    while not matched:
        # Add recipes
        newRecipes =  list(map(int, list(str(recipes[cursor1] + recipes[cursor2]))))
        recipes += newRecipes
        cursor1 = nextRecipe(recipes, cursor1)
        cursor2 = nextRecipe(recipes, cursor2)

        # Check new scores
        for i in range(len(newRecipes)):
            startIdx = len(recipes) - i - len(score)

            if startIdx >= 0:
                chars = map(lambda x: chr(x + ord('0')), recipes[startIdx : startIdx + len(score)])
                string = ''.join(list(chars))

                if score == string:
                    return startIdx

            # Print to track progress
            if startIdx % 1000000 == 0 and startIdx != 0:
                print(startIdx)


def nextRecipe(recipes, cursor):
    cursor += recipes[cursor] + 1
    cursor %= len(recipes)
    return cursor


if __name__ == "__main__":
    main()
