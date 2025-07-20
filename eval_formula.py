
class Node:
    def __init__(self, value: str, left: 'Node' = None, right: 'Node' = None):
        self.value = value
        self.left = left
        self.right = right

def evaluate(node: Node) -> bool:
    if node.value == '0':
        return False
    elif node.value == '1':
        return True
    elif node.value == '!':
        return not evaluate(node.left)
    elif node.value == '&':
        return evaluate(node.left) and evaluate(node.right)
    elif node.value == '|':
        return evaluate(node.left) or evaluate(node.right)
    elif node.value == '^':
        return evaluate(node.left) != evaluate(node.right)
    elif node.value == '>':
        return (not evaluate(node.left)) or evaluate(node.right)
    elif node.value == '=':
        return evaluate(node.left) == evaluate(node.right)
    else:
        raise ValueError(f"Opérateur inconnu : {node.value}")


def parse_rpn_to_ast(formula: str) -> Node:
    stack = []

    for ch in formula:
        if ch in '01':
            stack.append(Node(ch))
        elif ch == '!':
            operand = stack.pop()
            stack.append(Node(ch, left=operand))
        elif ch in '&|^>=':
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(ch, left=left, right=right))
        else:
            raise ValueError(f"Symbole non reconnu : {ch}")

    if len(stack) != 1:
        raise ValueError("Formule invalide")
    return stack.pop()
if __name__ == "__main__":
    test_formulas = [
        "10&",
        "10|",
        "11>",
        "10=",
        "1011||=",
        "1!",
        "0!",
        "11^",
    ]

    for formula in test_formulas:
        try:
            ast = parse_rpn_to_ast(formula)
            result = evaluate(ast)
            print(f"{result}")
        except Exception as e:
            print(f"Erreur : {e}")
