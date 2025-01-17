import random
import time

C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_RES = "\033[0m"

def adder(a: int, b: int) -> int:
    if a < 0 or b < 0:
            raise ValueError(f"{C_RED}Error: {C_RES}Unsigned int expected.")
    while (b != 0):
        carry = a & b
        a = a ^ b
        b = carry << 1
    return a

def check_time_complexity(f):
    input_sizes = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]
    res = []
    for n in input_sizes:
        start_time = time.time_ns()
        f(n, n)
        end_time = time.time_ns()
        execution_time = end_time - start_time
        res.append((n, execution_time))
    for i in range(0, len(res)):
        _, prev_time = res[i - 1]
        n, curr_time = res[i]
        if prev_time:
            ratio = curr_time / prev_time
            print(f"{C_BLUE}Size:{C_RES} {n}{C_BLUE}, Execution time: {C_RES}{curr_time}{C_BLUE}, Ratio: {C_RES}{ratio:.2f}")
        else:
            print(f"{C_BLUE}Size:{C_RES} {n}{C_BLUE}, Execution time: {C_RES}{curr_time}{C_BLUE}, Ratio: {C_RES}-")

def main():
    tests = [(0, 0), (4294967295, 4294967295)]
    for _ in range(10):
        tests.append((random.randrange(0, 100), random.randrange(0, 100)))
        tests.append((random.randrange(0, 2147483647), random.randrange(0, 2147483647)))
    for t in tests:
        try:
            x, y = t[0], t[1]
            res = adder(x, y)
            val = x + y
            if (res == val):
                print(f"{C_GREEN}{(res == val)}: {C_RES}{x} + {y} = {val} = {res}")
            else:
                print(f"{C_RED}{(res == val)}: {C_RES}{x} + {y} = {val} != {res}")
        except ValueError as e:
            print(e)
    # try:
    #    check_time_complexity(adder)
    # except ValueError as e:
    #         print(e)


if (__name__ == "__main__"):
    main()