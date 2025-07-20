import itertools

# Définition d'un noeud de l'arbre
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    # Fonction pour évaluer l'arbre récursivement
    def evaluate(self, valuation):
        if self.value.isalpha():
            return valuation[self.value]
        elif self.value == '!':
            return not self.left.evaluate(valuation)
        elif self.value == '&':
            return self.left.evaluate(valuation) and self.right.evaluate(valuation)
        elif self.value == '|':
            return self.left.evaluate(valuation) or self.right.evaluate(valuation)
        else:
            raise ValueError(f"Invalid operator: {self.value}")

# Fonction pour transformer RPN en arbre
def rpn_to_tree(rpn):
    stack = []
    for c in rpn:
        if c.isalpha():
            stack.append(Node(c))
        elif c == '!':
            if len(stack) < 1:
                raise ValueError("Invalid formula")
            node = stack.pop()
            stack.append(Node('!', left=node))
        elif c in '&|':
            if len(stack) < 2:
                raise ValueError("Invalid formula")
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(c, left=left, right=right))
        else:
            raise ValueError(f"Invalid character in formula: {c}")
    if len(stack) != 1:
        raise ValueError("Invalid formula")
    return stack[0]

# Fonction principale : SAT solver
def is_satisfiable(rpn):
    try:
        tree = rpn_to_tree(rpn)
    except ValueError as e:
        print(f"Error: {e}")
        return False

    variables = sorted(set(c for c in rpn if c.isalpha()))

    for values in itertools.product([False, True], repeat=len(variables)):
        valuation = dict(zip(variables, values))
        if tree.evaluate(valuation):
            return True 
    return False 


if __name__ == "__main__":
    examples = [
        "AB&",   # A AND B => satisfiable
        "AB|",   # A OR B => satisfiable
        "AA!&",  # A AND NOT A => always False
        "AA^",    # NOT A => satisfiable
    ]

    for formula in examples:
        result = is_satisfiable(formula)
        print(f"// {result}")

