C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_RES = "\033[0m"

def gray_code(a: int) -> int:
    calc = (a ^ (a << 1)) >> 1
    return calc

def check(a, b):
    res = gray_code(a)
    val = b
    if (res == val):
        print(C_GREEN, (res == val), C_RES, a, " = ", val, " = ", res)
    else:
        print(C_RED, (res == val), C_RES, a, " = ", val, " != ", res)

def main():
    test_subject = [(0, 0), (1, 1), (2, 3), (3, 2), (4, 6), (5, 7), (6, 5), (7, 4), (8, 12)]
    test_additional = [(86, 125), (99, 82), (100, 86), (128, 192), (2147483647, 1073741824)]
    for a, b in test_subject:
        check(a, b)
    for a, b in test_additional:
        check(a, b)

if (__name__ == "__main__"):
    main()