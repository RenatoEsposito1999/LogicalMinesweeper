class KnowledgeBase():
    # S means safe, B means mine, N means that cell contains number
    def __init__(self):
        self.propositions = set()
        self.rules = self.generate_rules()
    
    def add_proposition(self, proposition):
        self.propositions.add(proposition)
    

    def generate_rules(self):
        rules = []
        for i in range(6):
            for j in range(6):
                # Se una cella è sicura, non può avere una bomba
                rules.append(f"S_{i}_{j} -> NOT B_{i}_{j}")
                
                # Se una cella ha 0 bombe adiacenti, tutte le celle adiacenti sono sicure
                adj = self.adjacent_cells(i, j)
                if adj:
                    adj_cells = ' AND '.join([f"S_{x}_{y}" for x, y in adj])
                    rules.append(f"N_{i}_{j}_0 -> {adj_cells}")
                
                # Se una cella ha k bombe adiacenti, esattamente k delle celle adiacenti sono bombe
                for k in range(1, 9):
                    comb = self.combinations(adj, k)
                    comb_rules = ' OR '.join([' AND '.join([f"B_{x}_{y}" if (x,y) in c else f"NOT B_{x}_{y}" for x, y in adj]) for c in comb])
                    rules.append(f"N_{i}_{j}_{k} -> ({comb_rules})")
        return rules
    
    def adjacent_cells(self, i, j):
        adj = []
        for x in range(max(0, i-1), min(6, i+2)):
            for y in range(max(0, j-1), min(6, j+2)):
                if (x, y) != (i, j):
                    adj.append((x, y))
        return adj

    def combinations(self, elements, k):
        if k == 0:
            return [[]]
        if not elements:
            return []
        first, rest = elements[0], elements[1:]
        combs_with_first = [[first] + c for c in self.combinations(rest, k-1)]
        combs_without_first = self.combinations(rest, k)
        return combs_with_first + combs_without_first

    def __str__(self):
        return f"Knowledge Base: {self.propositions}"

'''# Esempio di utilizzo della KB
kb = KnowledgeBase()

#kb.add_proposition("S_0_0")
print("REGOLE")
for rule in kb.rules[:5]:
    print(rule)
print("----------------------------")
print("Supponendo che l'utente clicca sulla cella 0,0 e trova il numero 0 allora scopre:")
kb.add_proposition("N_0_0_0")
for rule in kb.propositions:
    print(type(rule))
#print(len(kb.propositions))
'''
'''# Nella KB in prop logic devo fare l'encode delle regole di gioco. 
# Proposizioni per le bombe nelle celle
def B(i, j):
    return f'B_{i}_{j}'

# Proposizioni per il numero di bombe adiacenti
def N(i, j, k):
    return f'N_{i}_{j}_{k}'

def generate_rules():
    rules = []
    for i in range(6):
        for j in range(6):
            # Regola: se c'è una bomba in (i, j), le celle adiacenti devono riflettere questo nel loro conteggio
            bomb_rule = f"{B(i, j)} -> ("
            adjacent_cells = []
            for x in range(max(0, i-1), min(6, i+2)):
                for y in range(max(0, j-1), min(6, j+2)):
                    if (x, y) != (i, j):
                        adjacent_cells.append(B(x, y))
            bomb_rule += ' + '.join(adjacent_cells) + ")"
            rules.append(bomb_rule)

            # Regole per il conteggio delle bombe adiacenti
            for k in range(9):
                count_rule = f"{N(i, j, k)} -> ("
                count_rule += ' + '.join([B(x, y) for x in range(max(0, i-1), min(6, i+2))
                                                      for y in range(max(0, j-1), min(6, j+2))
                                                      if (x, y) != (i, j)]) + f" = {k})"
                rules.append(count_rule)
    return rules

# Esempio di generazione delle regole
rules = generate_rules()
for rule in rules:
    print(rule)
print(len(rule))'''