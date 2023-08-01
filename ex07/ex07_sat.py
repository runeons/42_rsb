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

    ################ print tree ################

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
        self.generate()

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
    
    def _compute_sat(self, combination):
        comb_dict = dict(zip(self.variables, combination))
        new_input = self._replace_vars(comb_dict)
        ast = BooleanRpn(new_input)
        res = ast.compute()
        self.table.append((comb_dict, res))
        return res

    ################ generate combinations ################

    def _get_combinations(self):
        for i in range(2 ** self.var_nb):
            combination = []
            for j in range(self.var_nb):
                is_set = (i >> j) & 1
                combination.append(bool(is_set))
            yield combination # generateur, append implicite

    def _generate_combinations(self):
        combinations = list(self._get_combinations())
        return combinations
    
    ################ main function ################

    def generate(self):
        combinations = self._generate_combinations()
        for cb in combinations:
            self._compute_sat(cb)

    def generate_sat(self):
        combinations = self._generate_combinations()
        for cb in combinations:
            if (self._compute_sat(cb) == True):
                return True
        return False


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

class GenericRpn:
    def __init__(self, inp):
        self.input = inp
        self.allowed_vars = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
        self.operators = set(['!', '&', '|', '^', '>', '='])
        self.stack = []
        self.node = None
        self.operators_nb = 0
        self.vars_nb = 0
        self.create()

    def compute_sat(self):
        pass

    def create(self):
        chars = list(self.input)
        if len(chars) == 0:
            raise ValueError(f"{C_RED}Error:{C_RES} empty formula")
        for c in chars:
            if c in self.allowed_vars:
                self.vars_nb += 1
                self.node = Node(c)
                self.stack.append(self.node)
            elif c in self.operators:
                if c == '!':
                    if not self.stack:
                        raise ValueError(f"{C_RED}Error:{C_RES} insufficient operands for operator '!' in {self.input}")
                    right = self.stack.pop()
                    self.node = Node(c, right=right)
                else:
                    self.operators_nb += 1
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
        if self.operators_nb == 0 and self.vars_nb > 1:
            raise ValueError(f"{C_RED}Error:{C_RES} there should be at least one operator within '&', '|', '^', '>', '=' in {self.input}")

    ################ print tree ################

    def print(self, depth=15):
        print(C_BLUE + "Print tree: " + C_YELLOW + self.input, C_RES)
        self._print_node(self.node, depth)

    def _print_node(self, node, depth):
        # if node is not None:
        #     print(C_GREEN, "Node : ",  node.value, C_RES)
        #     if node.left is not None:
        #         print(C_GREEN, "Left : ", node.left.value, C_RES)
        #     if node.right is not None:
        #         print(C_GREEN, "Right : ", node.right.value, C_RES)
        if node is not None:
            if node.value == '!':
                print("  " * depth, C_YELLOW, node.value, C_RES)
            else:
                print("  " * depth, C_YELLOW, node.value, C_RES)
            self._print_node(node.left, depth - 2)
            self._print_node(node.right, depth + 2)

def main():
    npi_inputs = [
        "AB|", "AB&", "AA!&", "AA^" # subject
    ] 
    
    for npi in npi_inputs:
        try:
            tt = TruthTable(npi)
            res = tt.generate_sat()
            if (res == True):
                print(f"{C_GREEN}{npi}{C_RES} ==> {C_GREEN}{res}{C_RES}")
            else:
                print(f"{C_RED}{npi}{C_RES} ==> {C_RED}{res}{C_RES}")
        except ValueError as e:
            print(e)

if (__name__ == "__main__"):
    main()
