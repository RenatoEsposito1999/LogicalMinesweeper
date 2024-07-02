'''
VERIFICARE CHE LE REGOLE DELLE BOMBE SIANO SENSATE, PROBABILEMNTE DEVO APPLIKCARE L'INFERENZA PER OGNI CELLA CHE CONOSCO. 
'''
from random import randrange
import re
from library.utils import *
from library.logic import *
from itertools import combinations
from cell import Cell
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
    game = None # Minesweeper class object
    
    def __init__(self,height,width,n_mines, game) -> None:
        self.height = height
        self.width = width
        self.n_mines = n_mines
        self.game = game
        # build definite clauses
        self.generate_clauses()
        # add rules to kb
        self.build_kb()
        print("Initial KB's len: ",len(self.knowledge_base.clauses))
        for rule in self.knowledge_base.clauses[:10]:
            print(rule)
        print(len(self.clauses))

    def generate_clauses(self):
        for row in range(self.height):
            for col in range(self.width):
                neighbors = [
                    (row-1, col-1), (row-1, col), (row-1, col+1),
                    (row, col-1),             (row, col+1),
                    (row+1, col-1), (row+1, col), (row+1, col+1)
                ]
                # Filtra i vicini validi che non escono dai bordi del campo
                neighbors = [(x, y) for (x, y) in neighbors if 0 <= x < self.height and 0 <= y < self.width]
                num_neighbors = len(neighbors)
                # Rules for mines
                # Genera clausole per ogni possibile numero di bombe (da 1 a num_neighbors)
                for k in range(1, num_neighbors + 1):
                    for bomb_comb in combinations(neighbors, k):
                        non_bomb_neighbors = [n for n in neighbors if n not in bomb_comb]
                        if len(non_bomb_neighbors) == num_neighbors - k:
                            premise_parts = [f"N_{row}_{col}_{k}"]
                            # Aggiungi condizioni per i vicini che non sono bombe
                            if non_bomb_neighbors:
                                premise_parts.extend([f"N_{nx}_{ny}_0" for (nx, ny) in non_bomb_neighbors])
                            # Aggiungi la conseguenza per ogni bomba individuata
                            for (bx, by) in bomb_comb:
                                self.clauses.append(f"{' & '.join(premise_parts)} ==> B_{bx}_{by}")

    def add_knowledge(self,row,col,nearby):
        # N.B: quando arrivano delle coordinate so per certo che queste non sono bombe perché altrimenti il gioco non 
        # avrebbe mai raggiunto questa porzione di codice ma sarebbe semplicemente terminato il gioco.

        print("Lunghezza della kb prima dell'inferenza ",len(self.knowledge_base.clauses))
        # aggiungo l'informazione alla kb se non c'è già
        if expr(f'N_{row}_{col}_{nearby}') not in self.knowledge_base.clauses:
            self.knowledge_base.tell(expr(f'N_{row}_{col}_{nearby}'))
        #print("Clausola inserità nella: ",clauses)
        #processo di inferenza: possiamo inferire qualcosa dai vicini? Se si li aggiungiamo alle varie liste.
        self.inference(row,col,nearby)
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

    def get_valid_neighbors(self,row,col):
        neighbors = [
                    (row-1, col-1), (row-1, col), (row-1, col+1),
                    (row, col-1),             (row, col+1),
                    (row+1, col-1), (row+1, col), (row+1, col+1)
                ]
        neighbors = [(x, y) for (x, y) in neighbors if 0 <= x < self.height and 0 <= y < self.width]
        return neighbors
    
    def inference(self,row,col,nearby):
        
        neighbors = self.get_valid_neighbors(row,col)
        num_neighbors = len(neighbors)
        for (i, j) in neighbors:
            # se non ho informazioni su i,j cioè se non è un movimenti già fatto, o se so che non è una mina, ne che è un movimento sicuro 
            if (i, j) not in self.moves_made and (i, j) not in self.safe_movements and (i, j) not in self.mines:
                if nearby == 0:
                    '''
                    Se dovessi codificare in logica proposizionale anche le informazioni dei safe andrei a creare una quantità enorme di regole che complicherebbero le regole
                    per trovare le bombe, poichè queste regole rappresentano tutte le possibili combiniziazioni per cui il numero di regole cresce in maniera esponenziale
                    rispetto al numero di simboli. Possiamo vederlo come un trade-off.
                    '''
                    # se ho 0 vuol dire che i miei vicini sono sicuri.
                    self.safe_movements.add((i,j))
                    new_nearby = self.game.get_nearby_mines(Cell(i,j))
                    self.knowledge_base.tell(expr(f'N_{i}_{j}_{new_nearby}'))
                    self.inference(i, j, new_nearby)
                else: #nearby > 0
                    if pl_fc_entails(self.knowledge_base,expr(f'B_{i}_{j}')):
                        print(f'B_{i}_{j} è una bomba')
                        self.mines.add((i,j))
                        self.knowledge_base.tell(expr(f'B_{i}_{j}'))
                


    def make_safe_move(self):
        # Deve generare un movimento non fatto che la KB sa che è safe o che contiene un numero.
        if self.safe_movements: # Se ci sono movimenti sicuri
            for mov in self.safe_movements: # per ogni movimento
                if mov not in self.moves_made: # prendo il primo che non è stato già fatto
                    self.moves_made.add(mov)
                    self.safe_movements.remove(mov)
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
