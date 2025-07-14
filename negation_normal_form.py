def to_nnf(rpn_formula):
    """
    Convertit une formule en RPN en sa forme normale négative (NNF).
    Entrée : formule en RPN (str)
    Sortie : formule en RPN en NNF (str)
    """
    stack = []

    def negate(formula):
        # Applique la négation en NNF sur la formule RPN.
        # On regarde la formule :
        # - Si c'est une variable simple (longueur 1 et lettre majuscule), on met ! devant.
        # - Si c'est une négation déjà (commence par '!'), on enlève la négation (double négation).
        # - Sinon, si c'est une conjonction ou disjonction, on applique De Morgan.
        
        # Pour parser simplement, on considère la formule sous forme RPN, donc on traite de façon récursive.
        # Ici on va décomposer la formule pour appliquer la négation.
        # Mais vu que c'est du RPN, il est plus simple de représenter la formule en structure.

        # Pour simplifier la gestion, on va créer un parseur RPN en structure d'arbre.
        tree = rpn_to_tree(formula)
        nnf_tree = negate_tree(tree)
        return tree_to_rpn(nnf_tree)


    # On définit la structure d'arbre pour la formule
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val  # variable, !, &, |
            self.left = left
            self.right = right

        def __repr__(self):
            if self.val in ['!', '&', '|']:
                if self.val == '!':
                    return f"!{self.left}"
                else:
                    return f"({self.left} {self.val} {self.right})"
            else:
                return self.val

    def rpn_to_tree(rpn):
        stack = []
        for c in rpn:
            if c.isalpha():
                stack.append(Node(c))
            elif c == '!':
                if not stack:
                    raise ValueError("Invalid formula: negation with empty stack")
                node = stack.pop()
                stack.append(Node('!', left=node))
            elif c in ['&', '|']:
                if len(stack) < 2:
                    raise ValueError("Invalid formula: binary op with insufficient operands")
                right = stack.pop()
                left = stack.pop()
                stack.append(Node(c, left, right))
            else:
                raise ValueError(f"Invalid character: {c}")
        if len(stack) != 1:
            raise ValueError("Invalid formula: stack has more than one element at end")
        return stack[0]

    def negate_tree(node):
        # Applique la négation en NNF sur l'arbre donné
        if node.val.isalpha():
            # variable -> appliquer négation
            return Node('!', left=node)
        elif node.val == '!':
            # double négation !!A = A
            return node.left
        elif node.val == '&':
            # ¬(A ∧ B) = ¬A ∨ ¬B
            left_neg = negate_tree(Node('!', left=node.left))
            right_neg = negate_tree(Node('!', left=node.right))
            return Node('|', left_neg, right_neg)
        elif node.val == '|':
            # ¬(A ∨ B) = ¬A ∧ ¬B
            left_neg = negate_tree(Node('!', left=node.left))
            right_neg = negate_tree(Node('!', left=node.right))
            return Node('&', left_neg, right_neg)
        else:
            raise ValueError(f"Unknown node val: {node.val}")

    def to_nnf_tree(node):
        # Convertit un arbre en NNF (pousse les négations vers les variables)
        if node.val.isalpha():
            return node
        elif node.val == '!':
            # applique négation en NNF
            return negate_tree(node.left)
        elif node.val == '&':
            left_nnf = to_nnf_tree(node.left)
            right_nnf = to_nnf_tree(node.right)
            return Node('&', left_nnf, right_nnf)
        elif node.val == '|':
            left_nnf = to_nnf_tree(node.left)
            right_nnf = to_nnf_tree(node.right)
            return Node('|', left_nnf, right_nnf)
        else:
            raise ValueError(f"Unknown node val: {node.val}")

    def tree_to_rpn(node):
        # Convertit un arbre en RPN
        if node.val.isalpha():
            return node.val
        elif node.val == '!':
            return tree_to_rpn(node.left) + '!'
        else:  # & ou |
            return tree_to_rpn(node.left) + tree_to_rpn(node.right) + node.val

    # 1. Construire arbre à partir du RPN d'entrée
    tree = rpn_to_tree(rpn_formula)
    # 2. Convertir en NNF (pousser négations)
    nnf_tree = to_nnf_tree(tree)
    # 3. Retourner la formule en RPN
    return tree_to_rpn(nnf_tree)


# Exemple de fonction main pour tester
def main():
    exemples = [
        "AB&!",   # ¬(A ∧ B) -> A!B!|
        "AB|!",   # ¬(A ∨ B) -> A!B!&
        "AB|C&!", # ¬((A ∨ B) ∧ C) -> A!B!&C!|
        "A!",     # ¬A -> A!
        "A",      # A -> A
        "AB&",    # A ∧ B -> AB&
        "AB|",    # A ∨ B -> AB|
        "AB|C&",  # (A ∨ B) ∧ C -> AB|C&
        "AB!&",   # A ∧ ¬B -> AB!&
    ]

    for f in exemples:
        try:
            nnf = to_nnf(f)
            print(f"Input: {f} -> NNF: {nnf}")
        except Exception as e:
            print(f"Input: {f} -> Error: {e}")

if __name__ == "__main__":
    main()
