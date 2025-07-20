def evaluate_rpn(formula: str, sets: list[set]) -> set:
    # Vérification de base : nombre de variables vs. ensembles fournis
    letters_in_formula = {c for c in formula if c.isalpha()}
    if len(letters_in_formula) != len(sets):
        print("Erreur : Nombre d'ensembles fourni ne correspond pas aux variables utilisées.")
        return set()

    # Associer A, B, C... aux ensembles donnés
    variable_sets = {chr(ord('A') + i): s for i, s in enumerate(sets)}
    global_universe = set().union(*sets)

    stack = []

    for c in formula:
        if c.isalpha():
            stack.append(variable_sets[c])
        elif c == '!':
            a = stack.pop()
            stack.append(global_universe - a)  # complément
        elif c == '&':
            b = stack.pop()
            a = stack.pop()
            stack.append(a.intersection(b))
        elif c == '|':
            b = stack.pop()
            a = stack.pop()
            stack.append(a.union(b))
        elif c == '^':
            b = stack.pop()
            a = stack.pop()
            stack.append((a - b).union(b - a))  # XOR
        elif c == '>':
            b = stack.pop()
            a = stack.pop()
            stack.append(global_universe - a.union(b))  # implication
        elif c == '=':
            b = stack.pop()
            a = stack.pop()
            inter = a.intersection(b)
            union = global_universe - ((a - b).union(b - a))
            stack.append(inter.union(union))  # équivalence
        else:
            print(f"Erreur : caractère invalide '{c}' ignoré.")

    if len(stack) != 1:
        print("Erreur : Formule invalide, reste des éléments dans la pile.")
        return set()

    return stack.pop()


def main():
    A = {1, 2, 3}
    B = {3, 4, 5}
    formula = 'AB&'  # Négation de (A union B)
    result = evaluate_rpn(formula, [A, B])

    print(f"Formule : {formula}")
    print(f"A = {A}")
    print(f"B = {B}")
    print(f"Résultat final : {result}")


if __name__ == "__main__":
    main()
