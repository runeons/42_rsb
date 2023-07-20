import random
C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_RES = "\033[0m"

def adder(a, b):
    while (b != 0):
        carry = a & b
        addition = a ^ b
        a = addition
        b = carry << 1
    return a

def check(res, val, a, b):
    if (res == val):
        print(C_GREEN, (res == val), C_RES, a, " + ", b, " = ", res, " = ", val)
    else:
        print(C_RED, (res == val), C_RES, a, " + ", b, " != ", res, " != ", val)

def main():
    for _ in range(10):
        a = random.randrange(0, 2147483647)
        b = random.randrange(0, 2147483647)
        res = adder(a, b)
        val = a + b
        check(res, val, a, b)

if (__name__ == "__main__"):
    main()