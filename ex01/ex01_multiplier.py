import random
C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_RES = "\033[0m"

def adder(x: int, y: int) -> int:
    while (y != 0):
        carry = x & y
        addition = x ^ y
        x = addition
        y = carry << 1
    return x

def multiplier(x: int, y: int) -> int:
    if x < 0 or y < 0:
        raise ValueError(f"{C_RED}Error: {C_RES}Unsigned int expected.")
    res = 0
    while (y > 0):
        if (y & 1):
            res = adder(res, x)
        x = x << 1
        y = y >> 1
    return res

def main():
    tests = [(0, 0), (4294967295, 4294967295)]
    for _ in range(10):
        tests.append((random.randrange(0, 2147483647), random.randrange(0, 2147483647)))
    for t in tests:
        try:
            x, y = t[0], t[1]
            res = multiplier(x, y)
            val = x * y
            if (res == val):
                print(f"{C_GREEN}{(res == val)}: {C_RES}{x} * {y} = {val} = {res}")
            else:
                print(f"{C_RED}{(res == val)}: {C_RES}{x} * {y} = {val} != {res}")
        except ValueError as e:
            print(e)

if (__name__ == "__main__"):
    main()