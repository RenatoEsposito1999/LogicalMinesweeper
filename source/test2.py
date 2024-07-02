from itertools import combinations
from library.logic import *

class Minesweeper:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.safe_movements = set()
        self.mines = set()
        self.knowledge_base = PropDefiniteKB

    def generate_clauses(self):
        for i in range(self.height):
            for j in range(self.width):
                neighbors = [
                    (i-1, j-1), (i-1, j), (i-1, j+1),
                    (i, j-1),           (i, j+1),
                    (i+1, j-1), (i+1, j), (i+1, j+1)
                ]
                neighbors = [(x, y) for (x, y) in neighbors if 0 <= x < self.height and 0 <= y < self.width]
                num_neighbors = len(neighbors)

                # Regole per N_ij_0
                for (x, y) in neighbors:
                    self.knowledge_base.tell(expr('~N_%d_%d_0 | S_%d_%d' % (i, j, x, y)))

                # Regole per N_ij_k (k > 0)
                for k in range(1, num_neighbors + 1):
                    for subset in combinations(neighbors, k):
                        condition = " & ".join([f'~B_{x}_{y}' for (x, y) in subset])
                        safe_neighbors = [f'S_{x}_{y}' for (x, y) in neighbors if (x, y) not in subset]
                        
                        if safe_neighbors:
                            clause = Expr(f'N_{i}_{j}_{k} & {condition} => ' + ' | '.join(safe_neighbors))
                            self.knowledge_base.tell(clause)
                        
                        for mine in subset:
                            clause = Expr(f'N_{i}_{j}_{k} & {condition} => B_{mine[0]}_{mine[1]}')
                            self.knowledge_base.tell(clause)

                # Regole per identificare mine certe
                for k in range(1, num_neighbors + 1):
                    condition = " | ".join([f'~S_{x}_{y}' for (x, y) in neighbors])
                    clause = Expr(f'N_{i}_{j}_{k} & {condition} => B_{i}_{j}')
                    self.knowledge_base.tell(clause)

    def infer(self, row, col, infer_type="safe"):
        neighbors = [
            (row-1, col-1), (row-1, col), (row-1, col+1),
            (row, col-1),             (row, col+1),
            (row+1, col-1), (row+1, col), (row+1, col+1)
        ]
        neighbors = [(x, y) for (x, y) in neighbors if 0 <= x < self.height and 0 <= y < self.width]
        num_neighbors = len(neighbors)

        if infer_type == "safe":
            for (i, j) in neighbors:
                if (i != row or j != col) and ((i, j) not in self.moves_made) and ((i, j) not in self.safe_movements) and ((i, j) not in self.mines):
                    if pl_fc_entails(self.knowledge_base, expr(f'S_{i}_{j}')):
                        self.safe_movements.add((i, j))
                        self.knowledge_base.tell(expr(f'S_{i}_{j}'))
                        print(f"Cella ({i}, {j}) è sicura.")
        elif infer_type == "number":
            for k in range(num_neighbors + 1):
                if pl_fc_entails(self.knowledge_base, expr(f'N_{row}_{col}_{k}')):
                    self.knowledge_base.tell(expr(f'N_{row}_{col}_{k}'))
                    print(f"Cella ({row}, {col}) ha {k} mine attorno.")
                    return k
        elif infer_type == "mine":
            for (i, j) in neighbors:
                if (i != row or j != col) and ((i, j) not in self.moves_made) and ((i, j) not in self.safe_movements) and ((i, j) not in self.mines):
                    if pl_fc_entails(self.knowledge_base, expr(f'B_{i}_{j}')):
                        self.mines.add((i, j))
                        self.knowledge_base.tell(expr(f'B_{i}_{j}'))
                        print(f"Cella ({i}, {j}) è una mina.")
        return None

# Esempio di utilizzo
ms = Minesweeper(6, 6)
ms.generate_clauses()

# Aggiungere conoscenza iniziale (numeri già noti)
ms.knowledge_base.append(expr("N_3_0_1"))
ms.knowledge_base.append(expr("N_3_1_1"))
ms.knowledge_base.append(expr("N_3_2_1"))
ms.knowledge_base.append(expr("N_4_0_0"))
ms.knowledge_base.append(expr("N_4_1_0"))
ms.knowledge_base.append(expr("N_4_2_1"))
ms.knowledge_base.append(expr("N_4_3_2"))
ms.knowledge_base.append(expr("N_5_0_0"))
ms.knowledge_base.append(expr("N_5_1_0"))
ms.knowledge_base.append(expr("N_5_2_0"))
ms.knowledge_base.append(expr("N_5_3_1"))

# Inferire mine e celle sicure
ms.infer(3, 2, infer_type="mine")
ms.infer(4, 3, infer_type="mine")
ms.infer(4, 3, infer_type="safe")

# Stampa della knowledge base
for clause in ms.knowledge_base:
    print(clause)


'''from library.utils import *
from library.logic import *
from itertools import combinations
definite_clauses_KB = PropDefiniteKB()
clauses = ['(B & F)==>E', 
           '(A & E & F)==>G', 
           '(B & C)==>F', 
           '(A & B)==>D', 
           '(E & F)==>H', 
           '(H & I)==>J',
           'A', 
           'B', 
           'C',
            '(N_0_0_1 & ~S_0_1 | ~S_1_0 | ~S_1_1) ==> B_0_0'
            ]

for clause in clauses:
    definite_clauses_KB.tell(expr(clause))

for c in definite_clauses_KB:
    print(c)

pl_fc_entails(definite_clauses_KB, expr('G'))
'''