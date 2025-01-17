import time

C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_RES = "\033[0m"

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class BooleanRpn:
    def __init__(self, inp):
        self.input = inp
        self.allowed_vars = set(['0', '1'])
        self.operators = set(['!', '&', '|', '^', '>', '='])
        self.stack = []
        self.node = None
        self.create()

    def create(self):
        chars = list(self.input)
        for c in chars:
            if c in self.allowed_vars:
                self.node = Node(int(c))
                self.stack.append(self.node)
            elif c in self.operators:
                if c == '!':
                    if not self.stack:
                        raise ValueError(f"{C_RED}Error:{C_RES} insufficient operands for operator '!' in {self.input}")
                    operand = self.stack.pop()
                    self.node = Node(c, right=operand)
                else:
                    if len(self.stack) < 2:
                        raise ValueError(f"{C_RED}Error:{C_RES} insufficient operands for operator '{c}' in {self.input}")
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.node = Node(c, left, right)
                self.stack.append(self.node)
            else:
                raise ValueError(f"{C_RED}Error:{C_RES} undefined character {c} in {self.input}")
        if len(self.stack) > 1:
            raise ValueError(f"{C_RED}Error:{C_RES} invalid formula {self.input}")

    def compute(self, node=None):
        if node is None:
            node = self.node
        if isinstance(node.value, int):
            return int(node.value)
        if node.value == '!':
            r = self.compute(node.right)
            return bool(not r)
        else:
            l = self.compute(node.left)
            r = self.compute(node.right)
            if node.value == '&':
                return bool(l & r)
            elif node.value == '|':
                return bool(l | r)
            elif node.value == '^':
                return bool(l ^ r)
            elif node.value == '>':
                return bool((not l) or r)
            elif node.value == '=':
                return bool(l == r)

    def print(self, depth=15):
        print(C_BLUE + "Print tree: " + C_YELLOW + self.input, C_RES)
        self._print_node(self.node, depth)

    def _print_node(self, node, depth):
        if node is not None:
            print("  " * depth, C_YELLOW, node.value, C_RES)
            self._print_node(node.left, depth - 2)
            self._print_node(node.right, depth + 2)

def check_time_complexity(f):
    inputs = ["1", "10&", "10!&", "1011&&&", "1011&&!&", "10&10&10&10&&&&", "10&10&10&10&10&10&10&10&&&&&&&&"]
    res = []
    for inp in inputs:
        start_time = time.time_ns()
        f(inp)
        end_time = time.time_ns()
        execution_time = end_time - start_time
        res.append((len(inp), execution_time))
    for i in range(0, len(res)):
        _, prev_time = res[i - 1]
        n, curr_time = res[i]
        if prev_time:
            ratio = curr_time / prev_time
            print(f"{C_BLUE}Size:{C_RES} {n}{C_BLUE}, Execution time: {C_RES}{curr_time}{C_BLUE}, Ratio: {C_RES}{ratio:.2f}")
        else:
            print(f"{C_BLUE}Size:{C_RES} {n}{C_BLUE}, Execution time: {C_RES}{curr_time}{C_BLUE}, Ratio: {C_RES}-")

def eval_formula(formula: str) -> bool:
    ast = BooleanRpn(formula)
    # ast.print()
    return (ast.compute())

def main():
    npi_inputs = []
    tests = [
        ("11=", True),
        ("1011||=!", False),
        ("10&!", True),
        ("10=!", True),
        ("10|!", False),
        ("11=!", False),
        ("11>!", False),
    ]
    tests_subjects = [
        ("10&", False),
        ("10|", True),
        ("11>", True),
        ("10=", False),
        ("1011||=", True),
    ]
    for t in tests:
        npi_inputs.append(t)
    for t in tests_subjects:
        npi_inputs.append(t)
    for npi in npi_inputs:
        try:
            res = eval_formula(npi[0])
            expected = npi[1]
            if (res == expected):
                print(f"{C_GREEN}{(res == expected)}: {C_RES}{npi[0]} = {expected} = {res}")
            else:
                print(f"{C_RED}{(res == expected)}: {C_RES}{npi[0]} = {expected} != {res}")
        except ValueError as e:
            print(e)
    # try:
    #    check_time_complexity(eval_formula)
    # except ValueError as e:
    #         print(e)

if (__name__ == "__main__"):
    main()