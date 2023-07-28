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
        self.variables = self.get_variables()
        self.var_nb = len(self.variables)
        self.table = []
        self.generate()

    def get_variables(self):
        variables = set()
        for c in list(self.input):
            if c.isupper() and c not in variables:
                variables.add(c)
        return sorted(variables)
    
    def generate(self):
        combinations = self._generate_combinations()
        for cb in combinations:
            self._compute(cb)

    def _generate_combinations(self):
        combinations = list(self._get_combinations(self.var_nb))
        return combinations

    def _get_combinations(self, var_nb):
        for i in range(2 ** var_nb):
            combination = []
            for j in range(var_nb):
                is_set = (i >> j) & 1
                combination.append(bool(is_set))
            yield combination # generateur, append implicite

    def _compute(self, combination):
        comb_dict = dict(zip(self.variables, combination))
        new_input = self._replace_vars(comb_dict)
        ast = BooleanRpn(new_input)
        res = ast.compute()
        self.table.append((comb_dict, res))

    def _replace_vars(self, comb_dict):
        new_input = self.input
        for letter, boolean in comb_dict.items():
            new_input = new_input.replace(letter, str(int(boolean)))
        return new_input

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

    def create(self):
        chars = list(self.input)
        for c in chars:
            if c in self.allowed_vars:
                self.vars_nb += 1
                self.node = Node(c)
                self.stack.append(self.node)
            elif c in self.operators:
                if c == '!':
                    if not self.stack:
                        raise ValueError(f"{C_RED}Error:{C_RES} insufficient operands for operator '!'")
                    right = self.stack.pop()
                    self.node = Node(c, right=right)
                else:
                    self.operators_nb += 1
                    if len(self.stack) < 2:
                        raise ValueError(f"{C_RED}Error:{C_RES} insufficient operands for operator '{c}'")
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.node = Node(c, left, right)
                self.stack.append(self.node)
            else:
                raise ValueError(f"{C_RED}Error:{C_RES} undefined character {c} in {self.input}")
        if self.operators_nb == 0 and self.vars_nb > 1:
            raise ValueError(f"{C_RED}Error:{C_RES} there should be at least one operator within '&', '|', '^', '>', '=' in {self.input}")
        
    def _print_stack(self):
        for i in self.stack:
            print(C_GREEN, i.value, C_RES)

    def print(self, depth=15):
        print(C_BLUE + "Print tree: " + C_YELLOW + self.input, C_RES)
        self._print_node(self.node, depth)

    def _print_node(self, node, depth):
        if node is not None:
            print(C_GREEN, "Node : ",  node.value, C_RES)
            if node.left is not None:
                print(C_GREEN, "Left : ", node.left.value, C_RES)
            if node.right is not None:
                print(C_GREEN, "Right : ", node.right.value, C_RES)
        if node is not None:
            if node.value == '!':
                print("  " * depth, C_YELLOW, node.value, C_RES)
            else:
                print("  " * depth, C_YELLOW, node.value, C_RES)
            self._print_node(node.left, depth - 2)
            self._print_node(node.right, depth + 2)

class RPNtoNNF:
    def __init__(self, ast):
        self.init_ast = ast
        self.ast = ast
        self.stack = []
        self.start_operators = set(['!', '&', '|', '^', '>', '='])
        self.end_operators = set(['!', '&', '|'])
        self.allowed_vars = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])

    def print_node_debug(self, node, msg=""):
        print(C_YELLOW, msg, C_RES)
        if node is not None:
            print(C_YELLOW, "n=", node.value, C_RES)
        if node.left is not None:
            print(C_YELLOW, "l=", node.left.value, C_RES)
        if node.right is not None:
            print(C_YELLOW, "r=", node.right.value, C_RES)

    def _replace_equivalence(self, node):
        if node is not None:
            node.value = '&'
            init_left = None
            if node.left is not None:
                init_left = node.left
                new_node_left = Node('>', left=node.left, right=node.right)
                node.left = new_node_left
            if node.right is not None:
                new_node_right = Node('>', left=node.right, right=init_left)
                node.right = new_node_right

    def _replace_xor(self, node):
        if node is not None:
            node.value = '|'
            new_node_left = Node('&', left=node.left, right=Node('!', right=node.right))
            new_node_right = Node('&', left=Node('!', right=node.left), right=node.right)
            node.left = new_node_left
            node.right = new_node_right
        
    def _replace_implication(self, node):
        if node is not None:
            node.value = '|'
            if node.left is not None:
                new_node = Node('!')
                new_node.right = node.left
                node.left = new_node

    def _replace_and_not(self, node):
        if (node is not None) and (node.right is not None) and (node.right.value == '&'):
            node.value = '|'
            new_node_left = Node('!', right=node.right.left)
            new_node_right = Node('!', right=node.right.right)
            node.left = new_node_left
            node.right = new_node_right        

    def _replace_xor_not(self, node):
        if (node is not None) and (node.right is not None) and (node.right.value == '^'):
            node.value = '&'
            new_node_left = Node('>', left=node.right.left, right=node.right.right)
            new_node_right = Node('>', left=node.right.right, right=node.right.left)
            node.left = new_node_left
            node.right = new_node_right

    def _replace_implication_not(self, node):
        if (node is not None) and (node.right is not None) and (node.right.value == '>'):
            node.value = '&'
            new_node_left = node.right.left
            new_node_right = Node('!', right = node.right.right)
            node.left = new_node_left
            node.right = new_node_right

    def _replace_or_not(self, node):
        if (node is not None) and (node.right is not None) and (node.right.value == '|'):
            node.value = '&'
            new_node_left = Node('!', right=node.right.left)
            new_node_right = Node('!', right=node.right.right)
            node.left = new_node_left
            node.right = new_node_right

    def _replace_equals_not(self, node):
        if node is not None and (node.right is not None) and (node.right.value == '='):
            node.value = '|'
            new_node_left = Node('&', left=node.right.left, right=Node('!', right=node.right.right))
            new_node_right = Node('&', left=Node('!', right=node.right.left), right=node.right.right)
            node.left = new_node_left
            node.right = new_node_right
        

    def _replace_double_not(self, node):
        if (node is not None) and (node.right is not None) and (node.right.value == '!'):
            if (node.right.right):
                node.value = node.right.right.value
                new_node_left = node.right.right.left
                new_node_right = node.right.right.right
                node.left = new_node_left
                node.right = new_node_right
            else:
                raise ValueError(f"{C_RED}Error in conversion:{C_RES} insufficient operands for operator '!'")

    def _recursive_convert_each(self, node):
        if node is not None:
            if node.value == '=':
                self._replace_equivalence(node)
            elif node.value == '^':
                self._replace_xor(node)
            elif node.value == '>':
                self._replace_implication(node)
            elif node.value == '!':
                if node.right is not None and node.right.value not in self.allowed_vars:
                    if node.right.value == '|':
                        self._replace_or_not(node)
                    elif node.right.value == '^':
                        self._replace_xor_not(node)
                    elif node.right.value == '&':
                        self._replace_and_not(node)
                    elif node.right.value == '>':
                        self._replace_implication_not(node)
                    elif node.right.value == '!':
                        self._replace_double_not(node)
                    elif node.right.value == '=':
                        self._replace_equals_not(node)
                    else:
                        raise ValueError(f"{C_RED}Error:{C_RES} character {node.right.value} should not be followed by not (!) in {self.get_nnf_formula()}")
            self._recursive_convert_each(node.left)
            self._recursive_convert_each(node.right)
        return self.ast

    def _convert_to_nnf(self):
        self._recursive_convert_each(self.ast.node)

    def convert_and_get_nnf_formula(self):
        self._convert_to_nnf()
        return self._recursive_to_nnf_formula(self.ast.node)

    def _recursive_to_nnf_formula(self, node):
        if node is None:
            return ""
        if node.value not in self.start_operators:
            return node.value
        if node.value == '!':
            r = self._recursive_to_nnf_formula(node.right)
            return f"{r}!"
        l = self._recursive_to_nnf_formula(node.left)
        r = self._recursive_to_nnf_formula(node.right)
        if node.value in ['&', '|', '^', '>', '=']:
            return f"{l}{r}{node.value}"
        return ""

    # def _recursive_to_infix_formula(self, node):
    #     if node is None:
    #         return ""
    #     if node.value not in self.start_operators:
    #         return node.value
    #     if node.value == '!':
    #         return f"!{self._recursive_to_infix_formula(node.right)}"
    #     l = self._recursive_to_infix_formula(node.left)
    #     r = self._recursive_to_infix_formula(node.right)
    #     if node.value == '&':
    #         return f"({l} & {r})"
    #     elif node.value == '|':
    #         return f"({l} | {r})"
    #     elif node.value == '^':
    #         return f"({l} ^ {r})"
    #     elif node.value == '>':
    #         return f"({l} > {r})"
    #     elif node.value == '=':
    #         return f"({l} = {r})"
    #     return ""

    # def print_infix_formula(self):
    #         print(C_RED, "Infix : ", self._recursive_to_infix_formula(self.init_ast.node), C_RES)

    # def _recursive_to_npi_formula(self, node):
    #     if node is None:
    #         return ""
    #     if node.value not in self.start_operators:
    #         return node.value
    #     if node.value == '!':
    #         r = self._recursive_to_npi_formula(node.right)
    #         return f"{r}!"
    #     l = self._recursive_to_npi_formula(node.left)
    #     r = self._recursive_to_npi_formula(node.right)
    #     if node.value in ['&', '|', '^', '>', '=']:
    #         return f"{l}{r}{node.value}"
    #     return ""

    # def print_npi_formula(self):
    #     print(C_RED, "NPI   : ", self._recursive_to_npi_formula(self.init_ast.node), C_RES)

    def print_nnf_formula(self):
        print(C_BLUE, "NNF   : ", self._recursive_to_nnf_formula(self.ast.node), C_RES)

    def get_nnf_formula(self):
        ret = self._recursive_to_nnf_formula(self.ast.node)
        return ret

    def print(self, depth=15):
        print(C_BLUE + "Print NNF tree: init input " + C_YELLOW + self.init_ast.input, C_RES)
        self._print_node(self.ast.node, depth)

    def _print_node(self, node, depth):
        if node is not None:
            print(C_GREEN, "Node : ",  node.value, C_RES)
            if node.left is not None:
                print(C_GREEN, "Left : ", node.left.value, C_RES)
            if node.right is not None:
                print(C_GREEN, "Right : ", node.right.value, C_RES)
        if node is not None:
            if node.value == '!':
                print("  " * depth, C_YELLOW, node.value, C_RES)
            else:
                print("  " * depth, C_YELLOW, node.value, C_RES)
            self._print_node(node.left, depth - 2)
            self._print_node(node.right, depth + 2)
    
    def check_nnf_format(self, nnf: str):
        for i in range(len(nnf)):
            if nnf[i] not in self.end_operators and nnf[i] not in self.allowed_vars:
                raise ValueError(f"{C_RED}Error:{C_RES} character {nnf[i]} not allowed in nnf {nnf}")
            elif (nnf[i] == '!'):
                if i <= 0 or nnf[i - 1] not in self.allowed_vars:
                    raise ValueError(f"{C_RED}Error:{C_RES} not (!) should always follow a variable in nnf {nnf}")
        return True

    def is_nnf(self, nnf:str):
        for i in range(len(nnf)):
            if nnf[i] not in self.end_operators and nnf[i] not in self.allowed_vars:
                return False
            elif (nnf[i] == '!'):
                if i <= 0 or nnf[i - 1] not in self.allowed_vars:
                    return False
        return True

def main():
    npi_inputs = [
        "AB=", "AB>", "AB^", "AB|", "AB&", "AB!"
        "AB=!", "AB>!", "AB^!", "AB|!", "AB&!",
        "AB=AB==", "AB>AB>=", "AB^AB^=", "AB|AB|=", "AB&AB&=", "AB!AB!=",
        "AB=AB=>", "AB>AB>>", "AB^AB^>", "AB|AB|>", "AB&AB&>", "AB!AB!>",
        "AB=AB=^", "AB>AB>^", "AB^AB^^", "AB|AB|^", "AB&AB&^", "AB!AB!^",
        "AB=AB=|", "AB>AB>|", "AB^AB^|", "AB|AB||", "AB&AB&|", "AB!AB!|",
        "AB=AB=&", "AB>AB>&", "AB^AB^&", "AB|AB|&", "AB&AB&&", "AB!AB!&",
        "AB=AB=!", "AB>AB>!", "AB^AB^!", "AB|AB|!", "AB&AB&!",
        "AB|C&!", "A!B!|", "A!B|", "A!B!&", "A!!B!!>", "AB!^", "AB>A>", "AB>A>B>",
        "AB!", "A", "A!", "!A"
    ]
    for npi in npi_inputs:
        try:
            converter = RPNtoNNF(GenericRpn(npi))
            nnf = converter.convert_and_get_nnf_formula()
            tt_npi = TruthTable(npi)
            tt_nnf = TruthTable(nnf)
            # tt_npi.print()
            # tt_nnf.print()
            converter.check_nnf_format(nnf)
            if (tt_nnf.table == tt_npi.table):
                print(C_GREEN, "True:", npi, "gives", nnf, C_RES)
            else:
                print(C_RED, "False:", npi, "can not give", nnf, C_RES)
            # print()
        except ValueError as e:
            print(e)

if (__name__ == "__main__"):
    main()
