from library.utils import *
from library.logic import *
from itertools import combinations

def generate_clauses(n):
    clauses = []

    for i in range(n):
        for j in range(n):
            neighbors = [
                (i-1, j-1), (i-1, j), (i-1, j+1),
                (i, j-1),           (i, j+1),
                (i+1, j-1), (i+1, j), (i+1, j+1)
            ]
            neighbors = [(x, y) for (x, y) in neighbors if 0 <= x < n and 0 <= y < n]
            num_neighbors = len(neighbors)

            # Regole per N_ij_0
            for (x, y) in neighbors:
                clauses.append(f"N_{i}_{j}_0 ==> S_{x}_{y}")

            # Regole per N_ij_k (k > 0)
            for k in range(1, num_neighbors + 1):
                for subset in combinations(neighbors, k):
                    condition = " & ".join([f"B_{x}_{y}" for (x, y) in subset])
                    safe_neighbors = [f"S_{x}_{y}" for (x, y) in neighbors if (x, y) not in subset]
                    for safe_neighbor in safe_neighbors:
                        clauses.append(f"N_{i}_{j}_{k} & {condition} ==> {safe_neighbor}")
                    for mine in subset:
                        clauses.append(f"N_{i}_{j}_{k} & {condition} ==> B_{mine[0]}_{mine[1]}")

    return clauses

# Esempio di generazione delle regole per un campo 6x6
clauses = generate_clauses(6)
