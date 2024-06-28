from random import randrange
import re
from library.utils import *
from library.logic import *
from itertools import combinations

class Agent:
    knowledge_base = PropDefiniteKB()
    height = None
    width = None
    n_mines = None
    mines = set()
    moves_made = set()
    clauses = []
    safe_movements = set()

    def __init__(self,height,width,n_mines) -> None:
        self.height = height
        self.width = width
        self.n_mines = n_mines
        # build definite clauses
        self.generate_clauses()
        # add rules to kb
        self.build_kb()

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
                    self.clauses.append(f"N_{i}_{j}_0 ==> S_{x}_{y}")

                # Regole per N_ij_k (k > 0)
                for k in range(1, num_neighbors + 1):
                    for subset in combinations(neighbors, k):
                        condition = " & ".join([f"B_{x}_{y}" for (x, y) in subset])
                        safe_neighbors = [f"S_{x}_{y}" for (x, y) in neighbors if (x, y) not in subset]
                        for safe_neighbor in safe_neighbors:
                            self.clauses.append(f"N_{i}_{j}_{k} & {condition} ==> {safe_neighbor}")
                        for mine in subset:
                            self.clauses.append(f"N_{i}_{j}_{k} & {condition} ==> B_{mine[0]}_{mine[1]}")
    
    def add_knowledge(self,row,col,nearby):
        # N.B: quando arrivano delle coordinate so per certo che queste non sono bombe perché altrimenti il gioco non 
        # avrebbe mai raggiunto questa porzione di codice ma sarebbe semplicemente terminato il gioco.

        # fa il movimento e lo aggiungo al set dei movimenti fatti
        self.moves_made.add((row,col))
        # devo creare l'espressione per cui fare la tell
        clauses = self.build_expression(row,col,nearby)
        # aggiungo la clausesola alla kb
        self.knowledge_base.tell(expr(clauses))
        
        #processo di inferenza: possiamo inferire qualcosa dai vicini? Se si li aggiungiamo alle varie liste.
        self.inference(row,col)


    def inference(self,row,col):
        neighbors = []
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if (0 <= i < self.height) and (0 <= j < self.width) and (i != row or j != col):
                    # per ogni vicino posso inferire che è safe? se si aggiungolo alla lista safe.
                    # per ogni vicino posso inferire che è una bomba? aggiungilo alla lista bombe.
                    # per ogni vicino posso inferire che ha un numero? Aggiungo alla lista dei numeri.
                    # N.B: Fare attenzione al fatto che se è safe potrebbe essere anche nella N_ _ _
                    pass
        
    def build_expression(self,row,col,nearby):
        # N.B: quando arrivano delle coordinate so per certo che queste non sono bombe perché altrimenti il gioco non 
        # avrebbe mai raggiunto questa porzione di codice ma sarebbe semplicemente terminato il gioco.
        if nearby:
            return f'N_{row}_{col}_{nearby}'
        else:
            return f'S_{row}_{col}'

    def make_safe_move(self):
        # Deve generare un movimento non fatto che la KB sa che è safe o che contiene un numero.
        if self.safe_movements:
            print("C'è un movimento sicuro da fare")
        else:
            print("Return none")
            return (None,None)

    def make_random_move(self):
        spaces_left = (self.height * self.width) - (len(self.moves_made) + len(self.mines)) #no space. 
        if spaces_left == 0:
            return None
        while True:
            i = randrange(self.height)
            j = randrange(self.width)
            if (i, j) not in (self.moves_made) and ((i, j) not in self.mines):
                return i, j

    def build_kb(self):
        for c in self.clauses:
            self.knowledge_base.tell(expr(c))

    def get_value_from_string(self, s):
        pattern = r"[NS]_(\d+)_(\d+)(?:_(\d+))?"
        match = re.search(pattern, s)
        if match:
            N_or_S = match.group(0)[0]
            i = int(match.group(1))
            j = int(match.group(2))
            k = int(match.group(3)) if match.group(3) else None
            return N_or_S, i, j, k
        else:
            return None
        
