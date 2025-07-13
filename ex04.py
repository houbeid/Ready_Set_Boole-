import itertools

# AST Node classes
class ASTNode:
    pass

class Var(ASTNode):
    def __init__(self, name):
        self.name = name

class Const(ASTNode):
    def __init__(self, value):
        self.value = value

class Not(ASTNode):
    def __init__(self, child):
        self.child = child

class And(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Or(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Xor(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Implies(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Equiv(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

# Build AST from formula string
def build_ast(formula):
    stack = []
    for c in formula:
        if c == '0':
            stack.append(Const(False))
        elif c == '1':
            stack.append(Const(True))
        elif 'A' <= c <= 'Z':
            stack.append(Var(c))
        elif c == '!':
            a = stack.pop()
            stack.append(Not(a))
        elif c == '&':
            b = stack.pop()
            a = stack.pop()
            stack.append(And(a, b))
        elif c == '|':
            b = stack.pop()
            a = stack.pop()
            stack.append(Or(a, b))
        elif c == '^':
            b = stack.pop()
            a = stack.pop()
            stack.append(Xor(a, b))
        elif c == '>':
            b = stack.pop()
            a = stack.pop()
            stack.append(Implies(a, b))
        elif c == '=':
            b = stack.pop()
            a = stack.pop()
            stack.append(Equiv(a, b))
        else:
            raise ValueError(f"Caractère invalide : {c}")
    if len(stack) != 1:
        raise ValueError("Formule invalide")
    return stack[0]

# Évaluer l'AST pour un dictionnaire de valeurs
def eval_ast(node, env):
    if isinstance(node, Const):
        return node.value
    elif isinstance(node, Var):
        return env[node.name]
    elif isinstance(node, Not):
        return not eval_ast(node.child, env)
    elif isinstance(node, And):
        return eval_ast(node.left, env) and eval_ast(node.right, env)
    elif isinstance(node, Or):
        return eval_ast(node.left, env) or eval_ast(node.right, env)
    elif isinstance(node, Xor):
        return eval_ast(node.left, env) ^ eval_ast(node.right, env)
    elif isinstance(node, Implies):
        return not eval_ast(node.left, env) or eval_ast(node.right, env)
    elif isinstance(node, Equiv):
        return eval_ast(node.left, env) == eval_ast(node.right, env)

# Fonction principale
def print_truth_table(formula: str):
    # Extraire les variables en gardant l'ordre
    variables = sorted(set([c for c in formula if 'A' <= c <= 'Z']))

    try:
        ast = build_ast(formula)
    except ValueError as e:
        print(f"Erreur : {e}")
        return

    # En-tête
    header = " | ".join(variables) + " | = |"
    print(f"| {header}")
    print("|" + "---|" * (len(variables) + 1))

    # Générer toutes les combinaisons possibles (2^n)
    for values in itertools.product([False, True], repeat=len(variables)):
        env = dict(zip(variables, values))
        try:
            result = eval_ast(ast, env)
        except Exception as e:
            result = "?"
        row = " | ".join(str(int(env[var])) for var in variables)
        print(f"| {row} | {int(result)} |")

# Exemple d'utilisation
if __name__ == "__main__":
    print_truth_table("AB&C|")  # équivalent à (A ∧ B) ∨ C
