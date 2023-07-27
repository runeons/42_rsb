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

class GenericRpn:
    def __init__(self, inp):
        self.input = inp
        self.allowed_vars = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
        self.operators = set(['!', '&', '|', '^', '>', '='])
        self.stack = []
        self.node = None
        self.create()

    def create(self):
        chars = list(self.input)
        for c in chars:
            if c in self.allowed_vars:
                self.node = Node(c)
                self.stack.append(self.node)
            elif c in self.operators:
                if c == '!':
                    if not self.stack:
                        raise ValueError(f"{C_RED}Error:{C_RES} insufficient operands for operator '!'")
                    right = self.stack.pop()
                    self.node = Node(c, right=right)
                else:
                    if len(self.stack) < 2:
                        raise ValueError(f"{C_RED}Error:{C_RES} insufficient operands for operator '{c}'")
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.node = Node(c, left, right)
                self.stack.append(self.node)
            else:
                raise ValueError(f"{C_RED}Error:{C_RES} undefined character {c} in {self.input}")

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

    def check_nnf_format(self):
        pass

    def _replace_equivalence(self, node):
        print(C_YELLOW, "_replace_equivalence", C_RES)
        if node is not None:
            node.value = '&'
            if node.left is not None:
                new_node_left = Node('>')
                new_node_left.left = node.left
                new_node_left.right = node.right
                node.left = new_node_left
            if node.right is not None:
                new_node_right = Node('>', left=node.right, right=node.left)
                # new_node_right.left = node.right
                # new_node_right.right = node.left
                node.right = new_node_right

    def _replace_xor(self, node):
        print(C_YELLOW, "_replace_xor", C_RES)
        pass

    def _replace_implication(self, node):
        print(C_YELLOW, "_replace_implication", C_RES)
        if node is not None:
            node.value = '|'
            if node.left is not None:
                new_node = Node('!')
                new_node.right = node.left
                node.left = new_node

    def _replace_and_not(self, node):
        print(C_YELLOW, "_replace_and_not", C_RES)
        pass

    def _replace_or_not(self, node):
        print(C_YELLOW, "_replace_or_not", C_RES)
        pass

    def _replace_double_not(self, node):
        print(C_YELLOW, "_replace_double_not", C_RES)
        pass

    def _convert_once(self, node):
        self.print_nnf_formula()
        if node is not None:
            if node.value == '=':
                self._replace_equivalence(node)
            elif node.value == '^':
                self._replace_xor(node)
            elif node.value == '>':
                self._replace_implication(node)
            elif node.value == '&':
                if node.right is not None and node.right.value == '!':
                    self._replace_and_not(node)
            elif node.value == '|':
                if node.right is not None and node.right.value == '!':
                    self._replace_or_not(node)
            elif node.value == '!':
                if node.right is not None and node.right.value == '!':
                    self._replace_double_not(node)
        return self.ast

    def _recursive_convert(self, node):
        if node is not None:
            self._convert_once(node)
            self._convert_once(node.left)
            self._convert_once(node.right)        

    def convert_to_nnf(self):
        self._recursive_convert(self.ast.node)

    def _recursive_to_infix_formula(self, node):
        if node is None:
            return ""
        if node.value not in self.start_operators:
            return node.value
        if node.value == '!':
            return f"!{self._recursive_to_infix_formula(node.right)}"
        l = self._recursive_to_infix_formula(node.left)
        r = self._recursive_to_infix_formula(node.right)
        if node.value == '&':
            return f"({l} & {r})"
        elif node.value == '|':
            return f"({l} | {r})"
        elif node.value == '^':
            return f"({l} ^ {r})"
        elif node.value == '>':
            return f"({l} > {r})"
        elif node.value == '=':
            return f"({l} = {r})"
        return ""

    def print_infix_formula(self):
            print(C_RED, "Infix : ", self._recursive_to_infix_formula(self.init_ast.node), C_RES)

    def _recursive_to_npi_formula(self, node):
        if node is None:
            return ""
        if node.value not in self.start_operators:
            return node.value
        if node.value == '!':
            r = self._recursive_to_npi_formula(node.right)
            return f"{r}!"
        l = self._recursive_to_npi_formula(node.left)
        r = self._recursive_to_npi_formula(node.right)
        if node.value in ['&', '|', '^', '>', '=']:
            return f"{l}{r}{node.value}"
        return ""

    def print_npi_formula(self):
        print(C_RED, "NPI   : ", self._recursive_to_npi_formula(self.init_ast.node), C_RES)

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

    def print_nnf_formula(self):
        print(C_RED, "NNF   : ", self._recursive_to_nnf_formula(self.ast.node), C_RES)

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


def main():
    # npi_inputs = ["AB&!", "AB|!", "AB>", "AB=", "AB|C&!"]
    # npi_inputs = ["AB&!", "A!B!|", "AB>", "AB=", "A!B|"]
    # npi_inputs = ["AB>", "A!B|", "AB|!", "A!B!&"]
    npi_inputs = ["AB="]
    for npi in npi_inputs:
        try:
            npi_ast = GenericRpn(npi)
            # npi_ast.print()
            nnf = RPNtoNNF(npi_ast)
            # nnf.print()
            nnf.print_infix_formula()
            nnf.print_npi_formula()
            nnf.convert_to_nnf()
            # nnf.print()
            nnf.print_nnf_formula()
            print('\n\n')
            # converter = RPNtoNNF(npi)
            # nnf = converter.convert()
            # print(npi, " => ", nnf)
        except ValueError as e:
            print(e)

if (__name__ == "__main__"):
    main()
