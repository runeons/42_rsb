import random
C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_RES = "\033[0m"

def adder(a: int, b: int) -> int:
    while (b != 0):
        carry = a & b
        addition = a ^ b
        a = addition
        b = carry << 1
    return a

def multiplier(a: int, b: int) -> int:
    if a < 0 or b < 0:
        raise ValueError(f"{C_RED}Error: {C_RES}Unsigned int expected.")
    add = 0
    while (b > 0):
        if (b & 1):
            add += a
        a = a << 1
        b = b >> 1
    return add

def main():
    tests = [(0, 0), (4294967295, 4294967295)]
    for _ in range(10):
        tests.append((random.randrange(0, 2147483647), random.randrange(0, 2147483647)))
    for t in tests:
        try:
            a = t[0]
            b = t[1]
            res = multiplier(a, b)
            val = a * b
            if (res == val):
                print(f"{C_GREEN}{(res == val)}: {C_RES}{a} * {b} = {val} = {res}")
            else:
                print(f"{C_RED}{(res == val)}: {C_RES}{a} * {b} = {val} != {res}")
        except ValueError as e:
            print(e)

if (__name__ == "__main__"):
    main()