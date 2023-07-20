C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_RES = "\033[0m"

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def create_ast(input):
    booleans = set(['0', '1'])
    operators = set(['!', '&', '|', '^', '>', '='])
    stack = []
    chars = list(input)

    for c in chars:
        if c in booleans:
            node = Node(int(c))
            stack.append(node)
        elif c in operators:
            right = stack.pop()
            left = stack.pop()
            node = Node(c, left, right)
            stack.append(node)
        else:
            raise ValueError(f"{C_RED}Error:{C_RES} undefined character {c} in {input}")
    return stack.pop()

def evaluate_ast(node):
    if isinstance(node.value, int):
        return int(node.value)
    
    left_value = evaluate_ast(node.left)
    right_value = evaluate_ast(node.right)
    
    if node.value == '!':
        return bool(left_value != right_value)
    elif node.value == '&':
        return bool(left_value & right_value)
    elif node.value == '|':
        return bool(left_value | right_value)
    elif node.value == '>':
        return bool((not left_value) | right_value)
    elif node.value == '=':
        return bool(left_value == right_value)


def main():
    str_inputs = ["10&", "10=", "10|", "11=", "11>", "1011||="]
    for s in str_inputs:
        try:
            ast = create_ast(s)
            result = evaluate_ast(ast)
            print(s, " => ", result)
        except ValueError as e:
            print(e)

if (__name__ == "__main__"):
    main()