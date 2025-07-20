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
            node = stack.pop()
            stack.append(Node('!', left=node))
        elif c in '&|':
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(c, left, right))
    return stack[0]


def to_nnf(node):
    if node.value == '!':
        child = node.left
        if child.value == '!':
            return to_nnf(child.left)
        elif child.value == '&':
            return Node('|', to_nnf(Node('!', child.left)), to_nnf(Node('!', child.right)))
        elif child.value == '|':
            return Node('&', to_nnf(Node('!', child.left)), to_nnf(Node('!', child.right)))
        else:
            return Node('!', to_nnf(child))
    elif node.value in '&|':
        return Node(node.value, to_nnf(node.left), to_nnf(node.right))
    else:
        return node


def distribute(node):
    if node.value == '|':
        left = distribute(node.left)
        right = distribute(node.right)
        if left.value == '&':
            return Node('&',
                        distribute(Node('|', left.left, right)),
                        distribute(Node('|', left.right, right)))
        elif right.value == '&':
            return Node('&',
                        distribute(Node('|', left, right.left)),
                        distribute(Node('|', left, right.right)))
        else:
            return Node('|', left, right)
    elif node.value == '&':
        return Node('&', distribute(node.left), distribute(node.right))
    else:
        return node


def tree_to_rpn(node):
    if node.value.isalpha():
        return node.value
    elif node.value == '!':
        return tree_to_rpn(node.left) + '!'
    else:
        return tree_to_rpn(node.left) + tree_to_rpn(node.right) + node.value


def conjunctive_normal_form(rpn):
    ast = rpn_to_tree(rpn)
    nnf = to_nnf(ast)
    cnf = distribute(nnf)
    cnf_rpn = tree_to_rpn(cnf)
    return cnf_rpn


if __name__ == "__main__":
    print(f"// {conjunctive_normal_form("AB&!C!|")}")
if __name__ == "__main__":
    rpn = "AB&!C!|"
    try:
        print(f"// {conjunctive_normal_form(rpn)}")
    except Exception as e:
        print(f"Erreur sur {rpn}: {e}")
