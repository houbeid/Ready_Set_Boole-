def evaluate_rpn(formula: str, sets: list[list[int]]) -> list[int]:
    letters_in_formula = {c for c in formula if c.isalpha()}
    if len(letters_in_formula) != len(sets):
        print("Erreur : Nombre d'ensembles fourni ne correspond pas aux variables utilisées.")
        return []

    variable_sets = {chr(ord('A') + i): set(s) for i, s in enumerate(sets)}
    global_universe = set().union(*sets)

    stack = []

    for c in formula:
        if c.isalpha():
            stack.append(variable_sets[c])
        elif c == '!':
            a = stack.pop()
            stack.append(global_universe - a)
        elif c == '&':
            b = stack.pop()
            a = stack.pop()
            stack.append(a & b)
        elif c == '|':
            b = stack.pop()
            a = stack.pop()
            stack.append(a | b)
        elif c == '^':
            b = stack.pop()
            a = stack.pop()
            stack.append((a - b) | (b - a))
        elif c == '>':
            b = stack.pop()
            a = stack.pop()
            stack.append(global_universe - a | b)
        elif c == '=':
            b = stack.pop()
            a = stack.pop()
            stack.append(global_universe - ((a - b) | (b - a)))
        else:
            print(f"Erreur : caractère invalide '{c}' ignoré.")

    if len(stack) != 1:
        print("Erreur : Formule invalide, reste des éléments dans la pile.")
        return []

    return sorted(stack.pop())


def main():
    sets = [
        [0, 1, 2],
        [2, 3, 4]
    ]
    formula = 'AB|'
    result = evaluate_rpn(formula, sets)

    print(f"// {result}")


if __name__ == "__main__":
    main()
