class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def rpn_to_tree(rpn):
    stack = []
    for c in rpn:
        if c.isalpha():
            stack.append(Node(c))
        elif c == '!':
            stack.append(Node('!', left=stack.pop()))
        elif c in ['&', '|']:
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(c, left, right))
        else:
            raise ValueError(f"Invalid character: {c}")
    if len(stack) != 1:
        raise ValueError("Invalid formula")
    return stack[0]

def push_negation(node):
    if node.value == '!':
        child = node.left
        if child.value == '!':
            return push_negation(child.left)
        elif child.value == '&':
            return Node('|', push_negation(Node('!', child.left)), push_negation(Node('!', child.right)))
        elif child.value == '|':
            return Node('&', push_negation(Node('!', child.left)), push_negation(Node('!', child.right)))
        else:
            return Node('!', push_negation(child))
    elif node.value in '&|':
        return Node(node.value, push_negation(node.left), push_negation(node.right))
    else:
        return node

def tree_to_rpn(node):
    if node.value.isalpha():
        return node.value
    elif node.value == '!':
        return tree_to_rpn(node.left) + '!'
    else:
        return tree_to_rpn(node.left) + tree_to_rpn(node.right) + node.value

def negation_normal_form(rpn_formula):
    tree = rpn_to_tree(rpn_formula)
    nnf_tree = push_negation(tree)
    return tree_to_rpn(nnf_tree)

if __name__ == "__main__":
    rpn = "AB|C&!"
    try:
        print(f"// {negation_normal_form(rpn)}")
    except Exception as e:
        print(f"Erreur sur {rpn}: {e}")
