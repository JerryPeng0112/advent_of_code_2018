"""
Before entering program loop, r2 = 10551319
r5++ in inner loop, if > r2, r4++
r4 in outer loop, if > r2, exits program
Every inner loop, r1 = r5 * r4
if r1 == r2, r0 += r4, the only time r0 value is changed
Solve for all denominators of r2, and get the sum
"""

def main():

    r2 = 10551319
    r1 = 0
    for i in range(1, r2 + 1):
        if r2 % i == 0:
            r1 += i

    print(r1)


if __name__ == '__main__':
    main()
