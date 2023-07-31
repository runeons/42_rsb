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
    def __init__(self, formula, sets=None):
        self.formula = formula
        self.allowed_vars = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
        self.operators = set(['!', '&', '|', '^', '>', '='])
        ### to create generic ast ###
        self.stack = []
        self.node = None
        self.operators_nb = 0
        self.vars_nb = 0
        ### to compute ast with sets ###
        self.sets = sets
        self.used_vars = set()
        self.var_set_map = {}
        self.final_set = []
        ### create ###
        self.create()

    def compute(self, node=None):
        if node is None:
            node = self.node
        if isinstance(node.value, set):
            return set(node.value)
        if node.value == '!':
            r = self.compute(node.right)
            return set(self.final_set) - r
        else:
            l = self.compute(node.left)
            r = self.compute(node.right)
            if node.value == '&':
                return l & r # je peux modifier ici
            elif node.value == '|':
                return l | r
            elif node.value == '^':
                return l ^ r
            elif node.value == '>':
                return set(self.final_set) - l | r
            elif node.value == '=':
                return set(self.final_set) if l == r else []

    def _through_ast_replace_sets(self, node):
        if node is None:
            return
        if node.value in self.allowed_vars:
            node.value = self.var_set_map[node.value]
        self._through_ast_replace_sets(node.left)
        self._through_ast_replace_sets(node.right)

    def _create_variable_set_mapping(self):
        if len(self.used_vars) != len(self.sets):
            raise ValueError(f"{C_RED}Error: {C_RES}The number of variables and sets must be the same.")
        for var, value in zip(self.used_vars, self.sets):
            self.var_set_map[var] = value

    def replace_var_with_sets(self):
        self._create_variable_set_mapping()
        self._through_ast_replace_sets(self.node)

    def create(self):
        chars = list(self.formula)
        for c in chars:
            if c in self.allowed_vars:
                self.vars_nb += 1
                self.used_vars.add(c)
                self.node = Node(c)
                self.stack.append(self.node)
            elif c in self.operators:
                if c == '!':
                    if not self.stack:
                        raise ValueError(f"{C_RED}Error:{C_RES} insufficient operands for operator '!' in {self.formula}")
                    right = self.stack.pop()
                    self.node = Node(c, right=right)
                else:
                    self.operators_nb += 1
                    if len(self.stack) < 2:
                        raise ValueError(f"{C_RED}Error:{C_RES} insufficient operands for operator '{c}' in {self.formula}")
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.node = Node(c, left, right)
                self.stack.append(self.node)
            else:
                raise ValueError(f"{C_RED}Error:{C_RES} undefined character {c} in {self.formula}")
        if self.operators_nb == 0 and self.vars_nb > 1:
            raise ValueError(f"{C_RED}Error:{C_RES} there should be at least one operator within '&', '|', '^', '>', '=' in {self.formula}")

    ################ print tree ################

    def print(self, depth=15):
        print(C_BLUE + "Print tree: " + C_YELLOW + self.formula, C_RES)
        self._print_node(self.node, depth)

    def _print_node(self, node, depth):
        if node is not None:
            if node.value == '!':
                print("  " * depth, C_YELLOW, node.value, C_RES)
            else:
                print("  " * depth, C_YELLOW, node.value, C_RES)
            self._print_node(node.left, depth - 2)
            self._print_node(node.right, depth + 2)

def eval_set(formula: str, sets):
    ast = GenericRpn(formula, sets)
    ast.replace_var_with_sets()
    # ast.print()
    final_set = ast.compute()
    return final_set if len(final_set) else []

def main():
    try:
        tests = [
            ("AB&", ({0, 1, 2}, {0, 3, 4})),
            ("AB&", ({0, 1, 2}, {5, 3, 4})),
            ("AB|", ({0, 1, 2}, {0, 3, 4})),
            ("A!", ({0, 1, 2},)),
            ("AB^", ({0, 1, 2}, {0, 3, 4})),
        ]
        for f, sets in tests:
            print(f"{C_BLUE}Init sets:{C_RES}", end=" ")
            for s in sets:
                print(f"{C_BLUE}{s}{C_RES}", end=" ")
            print()
            print(f"{C_BLUE}Formula: {C_YELLOW}{f}{C_RES}")
            res = eval_set(f, sets)
            print(f"{C_BLUE}Result:  {C_YELLOW}{res}{C_RES}", end="\n\n")

    except ValueError as e:
        print(e)

if (__name__ == "__main__"):
    main()