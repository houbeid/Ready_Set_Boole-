
class Node:
    def __init__(self, value: str, left: 'Node' = None, right: 'Node' = None):
        self.value = value
        self.left = left
        self.right = right

    def evaluate(self) -> bool:
        if self.value == '0':
            return False
        elif self.value == '1':
            return True
        elif self.value == '!':
            return not self.left.evaluate()
        elif self.value == '&':
            return self.left.evaluate() and self.right.evaluate()
        elif self.value == '|':
            return self.left.evaluate() or self.right.evaluate()
        elif self.value == '^':
            return self.left.evaluate() != self.right.evaluate()
        elif self.value == '>':
            return (not self.left.evaluate()) or self.right.evaluate()
        elif self.value == '=':
            return self.left.evaluate() == self.right.evaluate()
        else:
            raise ValueError(f"Opérateur inconnu : {self.value}")

    # def pretty_print(self, indent=""):
    #     if self.right:
    #         self.right.pretty_print(indent + "   ")
    #     print(indent + self.value)
    #     if self.left:
    #         self.left.pretty_print(indent + "   ")


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
            result = ast.evaluate()
            print(f"{result}")
        except Exception as e:
            print(f"Erreur : {e}")
