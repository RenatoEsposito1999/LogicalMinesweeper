# PRIMA DI FARE LE MODIFICHE AI SIMBOLI
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
    clauses = []
    # Mine trovate 
    mines = set()
    # Movimenti fatti
    moves_made = set()
    # Movimenti sicuri, cioè con numero zero
    safe_movements = set()
    # movimenti sicuri, ma con numeri
    safe_movements_with_number = set()

    def __init__(self,height,width,n_mines) -> None:
        self.height = height
        self.width = width
        self.n_mines = n_mines
        # build definite clauses
        self.generate_clauses()
        # add rules to kb
        self.build_kb()
        print("Initial KB's len: ",len(self.knowledge_base.clauses))
        for rule in self.knowledge_base.clauses[100:150]:
            print(rule)




    def generate_clauses(self):
        for i in range(self.height):
            for j in range(self.width):
                neighbors = [
                    (i-1, j-1), (i-1, j), (i-1, j+1),
                    (i, j-1),       (i, j+1),
                    (i+1, j-1), (i+1, j), (i+1, j+1)
                ]
                neighbors = [(x, y) for (x, y) in neighbors if 0 <= x < self.height and 0 <= y < self.width]
                num_neighbors = len(neighbors)

                # Regole per N_i_j_0
                self.clauses.append(f"N_{i}_{j}_0 ==> S_{i}_{j}")
                for (x, y) in neighbors:
                    self.clauses.append(f"N_{i}_{j}_0 ==> S_{x}_{y}")
                    
                # Regole per N_i_j_k (k > 0)
                for k in range(1, num_neighbors + 1):
                    for subset in combinations(neighbors, k):
                        condition = " & ".join([f"B_{x}_{y}" for (x, y) in subset])
                        safe_neighbors = [f"S_{x}_{y}" for (x, y) in neighbors if (x, y) not in subset]
                        for safe_neighbor in safe_neighbors:
                            self.clauses.append(f"N_{i}_{j}_{k} & {condition} ==> {safe_neighbor}")
                        for mine in subset:
                            self.clauses.append(f"N_{i}_{j}_{k} & {condition} ==> B_{mine[0]}_{mine[1]}")
                # Regole per bomba
                for k in range(1, len(neighbors) + 1):
                    condition = " & ".join([f'S_{x}_{y}' for (x, y) in neighbors])
                    self.clauses.append(f'N_{i}_{j}_{k} & {condition} ==> B_{i}_{j}')

        '''for k in range(1, num_neighbors + 1):
                    condition = " & ".join([f'~S_{x}_{y}' for (x, y) in neighbors])
                    self.knowledge_base.append(expr(f'N_{i}_{j}_{k}') & expr(condition) >> expr(f'B_{i}_{j}'))'''
        '''for i in range(self.height):
            for j in range(self.width):
                neighbors = [
                    (i-1, j-1), (i-1, j), (i-1, j+1),
                    (i, j-1),           (i, j+1),
                    (i+1, j-1), (i+1, j), (i+1, j+1)
                ]
                neighbors = [(x, y) for (x, y) in neighbors if 0 <= x < self.height and 0 <= y < self.width]
                num_neighbors = len(neighbors)

                # Regole per N_i_j_0
                for (x, y) in neighbors:
                    self.clauses.append(expr(f'N_{i}_{j}_0') >> expr(f'S_{x}_{y}'))

                # Regole per N_i_j_k (k > 0)
                for k in range(1, num_neighbors + 1):
                    for subset in combinations(neighbors, k):
                        condition = expr(" & ".join([f'B_{x}_{y}' for (x, y) in subset]))
                        safe_neighbors = [expr(f'S_{x}_{y}') for (x, y) in neighbors if (x, y) not in subset]
                        for safe_neighbor in safe_neighbors:
                            self.clauses.append(expr(f'N_{i}_{j}_{k}') & condition >> safe_neighbor)
                        for mine in subset:
                            self.clauses.append(expr(f'N_{i}_{j}_{k}') & condition >> expr(f'B_{mine[0]}_{mine[1]}'))

                # Regole per identificare mine certe
                for k in range(1, num_neighbors + 1):
                    condition = " & ".join([f'~S_{x}_{y}' for (x, y) in neighbors])
                    self.clauses.append(expr(f'N_{i}_{j}_{k}') & expr(condition) >> expr(f'B_{i}_{j}'))
        '''





    def add_knowledge(self,row,col,nearby):
        # N.B: quando arrivano delle coordinate so per certo che queste non sono bombe perché altrimenti il gioco non 
        # avrebbe mai raggiunto questa porzione di codice ma sarebbe semplicemente terminato il gioco.

        # devo creare l'espressione per cui fare la tell
        #clauses = self.build_expression(row,col,nearby)
        # aggiungo la clausesola alla kb
        print("Lunghezza della kb prima dell'inferenza ",len(self.knowledge_base.clauses))
        self.knowledge_base.tell(expr(f'N_{row}_{col}_{nearby}'))
        #print("Clausola inserità nella: ",clauses)
        #processo di inferenza: possiamo inferire qualcosa dai vicini? Se si li aggiungiamo alle varie liste.
        self.inference(row,col)
        self.print(title='[Agent] new informations after inference process')

    '''def inference(self,row,col):
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                # se il vicino è nel campo (quindi è valido) e non è già stato selezionato come movimento fatto o se non si hanno già informazioni
                if (0 <= i < self.height) and (0 <= j < self.width) and (i != row or j != col) and ((i,j) not in self.moves_made) and ((i,j) not in self.safe_movements) and ((i,j) not in self.mines):
    
                    # per ogni vicino posso inferire che è safe? se si aggiungolo alla lista safe.'
                    if pl_fc_entails(self.knowledge_base,expr(f'S_{i}_{j}')):
                        self.safe_movements.add((i,j))
                    # per ogni vicino posso inferire che è una bomba? aggiungilo alla lista bombe.
                    # per ogni vicino posso inferire che ha un numero? Aggiungo alla lista dei numeri.
                    elif pl_fc_entails(self.knowledge_base,expr(f'N_{i}_{j}')): # E' da capire come codificare questooooooooooooooooooo
                        self.safe_movements_with_number.add((i,j))
                    elif pl_fc_entails(self.knowledge_base,expr(f'B_{i}_{j}')):
                        self.mines.add((i,j))
                    # N.B: Fare attenzione al fatto che se è safe potrebbe essere anche nella N_ _ _
                
                # alla fine del processo agigungiamo il movimento come fatto
                self.moves_made.add((row,col))
    '''
    
    def inference(self,row,col):
        neighbors = [
                    (row-1, col-1), (row-1, col), (row-1, col+1),
                    (row, col-1),             (row, col+1),
                    (row+1, col-1), (row+1, col), (row+1, col+1)
                ]
        neighbors = [(x, y) for (x, y) in neighbors if 0 <= x < self.height and 0 <= y < self.width]
        num_neighbors = len(neighbors)

        for (i, j) in neighbors:
            if (i != row or j != col) and ((i, j) not in self.moves_made) and ((i, j) not in self.safe_movements) and ((i, j) not in self.mines):
                if pl_fc_entails(self.knowledge_base, expr(f'S_{i}_{j}')):
                    self.safe_movements.add((i, j))
                    self.knowledge_base.tell(expr(f'S_{i}_{j}'))
                if pl_fc_entails(self.knowledge_base, expr(f'B_{i}_{j}')):
                    print("E' una bomba")
                    self.knowledge_base.tell(expr(f'B_{i}_{j}'))
                    self.mines.add((i, j))
                '''if self.bc(self.knowledge_base,expr(f'S_{i}_{j}')):
                    self.safe_movements.add((i, j))
                    self.knowledge_base.tell(expr(f'S_{i}_{j}'))'''

        #return None 



    def make_safe_move(self):
        # Deve generare un movimento non fatto che la KB sa che è safe o che contiene un numero.
        if self.safe_movements: # Se ci sono movimenti sicuri
            for mov in self.safe_movements: # per ogni movimento
                if mov not in self.moves_made: # prendo il primo che non è stato già fatto
                    self.moves_made.add(mov)
                    self.safe_movements.remove(mov)
                    return mov
        elif self.safe_movements_with_number:
            for mov in self.safe_movements_with_number: # per ogni movimento
                if mov not in self.moves_made: # prendo il primo che non è stato già fatto
                    self.moves_made.add(mov)
                    self.safe_movements_with_number.remove(mov)
                    return mov
        else:
            return (None,None)

# ragionare se posso usare concetti di probabilità per selezionare elementi con una probabilità minore.
    def make_random_move(self):
        spaces_left = (self.height * self.width) - (len(self.moves_made) + len(self.mines)) #no space. 
        if spaces_left == 0:
            return None
        while True:
            i = randrange(self.height)
            j = randrange(self.width)
            if (i, j) not in (self.moves_made) and ((i, j) not in self.mines):
                # fa il movimento e lo aggiungo al set dei movimenti fatti
                self.moves_made.add((i,j))
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
        
    def bc(self,kb,query):
        if query in kb.clauses:
            return True
        
        for clause in kb.clauses:
            if isinstance(clause, Expr) and clause.op == "==>" and clause.args[1] == query:
                premises = conjuncts(clause.args[0])
                if all(self.bc(kb,premise) for premise in premises):
                    return True

        return False

    def print(self,title):
        print(title)
        print("[Agent]: Safe movements:")
        string = ""
        for mov in self.safe_movements:
            if mov not in self.moves_made:
                string+=f'{mov} '
        print(string)
        print("[Agent]: Knowed mines:")
        string = ""
        for mov in self.mines:
            string+=f'{mov} '
        print(string)
        print("[Agent]: Movements already made:")
        string = ""
        for mov in self.moves_made:
            string+=f'{mov} '
        print(string)
        print("Len of KB: ", len(self.knowledge_base.clauses))
        print("-------------------------------------------------------------------")
