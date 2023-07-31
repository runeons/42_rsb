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

# class BooleanRpn:
#     def __init__(self, inp):
#         self.input = inp
#         self.allowed_vars = set(['0', '1'])
#         self.operators = set(['!', '&', '|', '^', '>', '='])
#         self.stack = []
#         self.node = None
#         self.create()

#     def create(self):
#         chars = list(self.input)
#         for c in chars:
#             if c in self.allowed_vars:
#                 self.node = Node(int(c))
#                 self.stack.append(self.node)
#             elif c in self.operators:
#                 if c == '!':
#                     if not self.stack:
#                         raise ValueError(f"{C_RED}Error:{C_RES} insufficient operands for operator '!' in {self.input}")
#                     operand = self.stack.pop()
#                     self.node = Node(c, right=operand)
#                 else:
#                     if len(self.stack) < 2:
#                         raise ValueError(f"{C_RED}Error:{C_RES} insufficient operands for operator '{c}' in {self.input}")
#                     right = self.stack.pop()
#                     left = self.stack.pop()
#                     self.node = Node(c, left, right)
#                 self.stack.append(self.node)
#             else:
#                 raise ValueError(f"{C_RED}Error:{C_RES} undefined character {c} in {self.input}")
    
#     def compute(self, node=None):
#         if node is None:
#             node = self.node
#         if isinstance(node.value, int):
#             return int(node.value)
#         if node.value == '!':
#             r = self.compute(node.right)
#             return bool(not r)
#         else:
#             l = self.compute(node.left)
#             r = self.compute(node.right)
#             if node.value == '&':
#                 return bool(l & r)
#             elif node.value == '|':
#                 return bool(l | r)
#             elif node.value == '^':
#                 return bool(l ^ r)
#             elif node.value == '>':
#                 return bool((not l) or r)
#             elif node.value == '=':
#                 return bool(l == r)

#     ################ print tree ################

#     def print(self, depth=15):
#         print(C_BLUE + "Print tree: " + C_YELLOW + self.input, C_RES)
#         self._print_node(self.node, depth)

#     def _print_node(self, node, depth):
#         if node is not None:
#             print("  " * depth, C_YELLOW, node.value, C_RES)
#             self._print_node(node.left, depth - 2)
#             self._print_node(node.right, depth + 2)

# class TruthTable:
#     def __init__(self, inp):
#         self.input = inp
#         self.variables = self.get_variables()
#         self.var_nb = len(self.variables)
#         self.table = []
#         self.generate()

#     def get_variables(self):
#         variables = set()
#         for c in list(self.input):
#             if c.isupper() and c not in variables:
#                 variables.add(c)
#         return sorted(variables)
    
#     ################ compute truth table ################

#     def _replace_vars(self, comb_dict):
#         new_input = self.input
#         for letter, boolean in comb_dict.items():
#             new_input = new_input.replace(letter, str(int(boolean)))
#         return new_input
    
#     def _compute(self, combination):
#         comb_dict = dict(zip(self.variables, combination))
#         new_input = self._replace_vars(comb_dict)
#         ast = BooleanRpn(new_input)
#         res = ast.compute()
#         self.table.append((comb_dict, res))

#     ################ generate combinations ################

#     def _get_combinations(self):
#         for i in range(2 ** self.var_nb):
#             combination = []
#             for j in range(self.var_nb):
#                 is_set = (i >> j) & 1
#                 combination.append(bool(is_set))
#             yield combination # generateur, append implicite

#     def _generate_combinations(self):
#         combinations = list(self._get_combinations())
#         return combinations
    
#     ################ main function ################

#     def generate(self):
#         combinations = self._generate_combinations()
#         for cb in combinations:
#             self._compute(cb)

#     ################ print truth table ################

#     def print(self):
#         print(C_BLUE + "Print truth table: " + C_YELLOW + self.input, C_RES)
#         self._print_sep_line()
#         for v in self.variables:
#             print(f"|  {v}  ", end='')
#         print(f"|  =  |")
#         self._print_sep_line()
#         for row in self.table:
#             for v in self.variables:
#                 print(f"|  {int(row[0][v])}  ", end='')
#             print(f"|  {int(row[1])}  |")
#         self._print_sep_line()
    
#     def _print_sep_line(self):
#         for _ in self.variables:
#             print(f"|-----", end='')
#         print(f"|-----|")

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