C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_RES = "\033[0m"

def gray_code(n: int) -> int:
    if n < 0 :
        raise ValueError(f"{C_RED}Error: {C_RES}Unsigned int expected.")
    res = (n ^ (n << 1)) >> 1
    return res

def main():
    tests = ([(86, 125), (99, 82), (100, 86), (128, 192), (2147483647, 1073741824), (4294967294, 2147483649), (4294967295, 2147483648)])
    tests_subjects = [(0, 0), (1, 1), (2, 3), (3, 2), (4, 6), (5, 7), (6, 5), (7, 4), (8, 12)] # subject
    for t in tests_subjects:
        tests.append(t)
    for t in tests:
        try:
            res = gray_code(t[0])
            expected = t[1]
            if (res == expected):
                print(f"{C_GREEN}{(res == expected)}: {C_RES}{t[0]} = {expected} = {res}")
            else:
                print(f"{C_RED}{(res == expected)}: {C_RES}{t[0]} = {expected} != {res}")
        except ValueError as e:
            print(e)


if (__name__ == "__main__"):
    main()