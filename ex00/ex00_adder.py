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

def check(a, b):
    res = adder(a, b)
    val = a + b
    if (res == val):
        print(C_GREEN, (res == val), C_RES, a, " + ", b, " = ", val, " = ", res)
    else:
        print(C_RED, (res == val), C_RES, a, " + ", b, " = ", val, " != ", res)

def main():
    test_limits = [(0, 0), (2147483647, 2147483647)]
    for a, b in test_limits:
        check(a, b)
    for _ in range(10):
        a = random.randrange(0, 2147483647)
        b = random.randrange(0, 2147483647)
        check(a, b)

if (__name__ == "__main__"):
    main()