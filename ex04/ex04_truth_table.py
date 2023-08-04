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
        if len(chars) == 0:
            raise ValueError(f"{C_RED}Error:{C_RES} empty formula")
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

class TruthTable:
    def __init__(self, inp):
        self.input = inp
        self.variables = self._get_variables()
        self.var_nb = len(self.variables)
        self.table = []

    def _get_variables(self):
        variables = set()
        for c in list(self.input):
            if c.isupper() and c not in variables:
                variables.add(c)
        return sorted(variables)

    ################ compute truth table ################

    def _replace_vars(self, comb_dict):
        new_input = self.input
        for letter, boolean in comb_dict.items():
            new_input = new_input.replace(letter, str(int(boolean)))
        return new_input
    
    def _compute(self, combination):
        comb_dict = dict(zip(self.variables, combination))
        new_input = self._replace_vars(comb_dict)
        ast = BooleanRpn(new_input)
        res = ast.compute()
        self.table.append((comb_dict, res))

    ################ generate combinations ################

    def _generate_combinations(self):
        combinations = list(self._get_combinations())
        return combinations

    def _get_combinations(self):
        for i in range(2 ** self.var_nb):
            combination = []
            for j in range(self.var_nb):
                is_set = (i >> j) & 1
                combination.append(bool(is_set))
            yield combination # generateur, append implicite

    ################ main function ################

    def generate(self):
        combinations = self._generate_combinations()
        for cb in combinations:
            self._compute(cb)

    ################ print truth table ################

    def print(self):
        print(C_BLUE + "Print truth table: " + C_YELLOW + self.input, C_RES)
        self._print_sep_line()
        for v in self.variables:
            print(f"|  {v}  ", end='')
        print(f"|  =  |")
        self._print_sep_line()
        for row in self.table:
            for v in self.variables:
                print(f"|  {int(row[0][v])}  ", end='')
            print(f"|  {int(row[1])}  |")
        self._print_sep_line()
    
    def _print_sep_line(self):
        for _ in self.variables:
            print(f"|-----", end='')
        print(f"|-----|")

def check_time_complexity(f):
    inputs = ["A", "AB&", "AB!&", "ABCA&&&", "ABCD&&!&", "AB&CD&EF&GH&&&&", "AB&CD&EF&GH&IJ&KL&AB&CD&&&&&&&&"]
    res = []
    for inp in inputs:
        start_time = time.time_ns()
        print_truth_table(inp)
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

def print_truth_table(formula: str):
    tt = TruthTable(formula)
    tt.generate()
    tt.print()

def main():
    npi_inputs = [
        # "AB=", "AB>", "AB^", "AB|", "AB&",
        # "AB|C&!", "A!B!|", "ABAA||=",
        "AB&C|" # subject,
        # "AB^", "AB!&A!B&|", "",
        # "B", "B!B!|A&", "AA|!B&",
        # "AB!", "!A", "AB&C!|>", "AA", "AB&c",          # invalid formula
        # "ABAA||=", "AB&CD&E||",
    ]
    for npi in npi_inputs:
        try:
            print_truth_table(npi)
        except ValueError as e:
            print(e)
    # try:
    #    check_time_complexity(print_truth_table)
    # except ValueError as e:
    #         print(e)

if (__name__ == "__main__"):
    main()