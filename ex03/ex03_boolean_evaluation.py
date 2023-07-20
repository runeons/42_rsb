C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_RES = "\033[0m"

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class Ast:
    def __init__(self, inp):
        self.input = inp
        self.booleans = set(['0', '1'])
        self.operators = set(['!', '&', '|', '^', '>', '='])
        self.stack = []
        self.node = None

    def create(self):
        chars = list(self.input)
        for c in chars:
            if c in self.booleans:
                self.node = Node(int(c))
                self.stack.append(self.node)
            elif c in self.operators:
                right = self.stack.pop()
                left = self.stack.pop()
                self.node = Node(c, left, right)
                self.stack.append(self.node)
            else:
                raise ValueError(f"{C_RED}Error:{C_RES} undefined character {c} in {input}")
    
    def evaluate(self, node=None):
        if node is None:
            node = self.node

        if isinstance(node.value, int):
            return int(node.value)
        
        l = self.evaluate(node.left)
        r = self.evaluate(node.right)
        
        if node.value == '!':
            return bool(l != r)
        elif node.value == '&':
            return bool(l & r)
        elif node.value == '|':
            return bool(l | r)
        elif node.value == '>':
            return bool((not l) or r)
        elif node.value == '=':
            return bool(l == r)

def main():
    str_inputs = ["10&", "10=", "10|", "11=", "11>", "1011||="]
    for s in str_inputs:
        try:
            ast = Ast(s)
            ast.create()
            result = ast.evaluate()
            print(s, " => ", result)
        except ValueError as e:
            print(e)

if (__name__ == "__main__"):
    main()