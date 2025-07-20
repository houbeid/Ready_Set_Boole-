from typing import List
import itertools

def powerset(input_set: List[int]) -> List[List[int]]:
    result = []
    n = len(input_set)
    for k in range(n + 1):
        for subset in itertools.combinations(input_set, k):
            result.append(list(subset))
    return result
    

if __name__ == "__main__":
    A = [1, 2, 3]
    B = powerset(A)
    print("Powerset of", A)
    for subset in B:
        print(subset)
