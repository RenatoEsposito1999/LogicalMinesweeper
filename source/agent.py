import re
from knowledge import KnowledgeBase
from random import randrange
class Agent:
    def __init__(self, height, width):
        print("INIZIO -------------------------------------------------------------------------------------------------------------")
        self.height = height
        self.width = width
        self.knowledge_base = KnowledgeBase(height, width)
        self.safe_movements = set()
        self.moves_made = set()
        self.mines = set()

    def update_kb(self):
        while True:
            new_propositions = set()
            for rule in self.knowledge_base.rules:
                premise, conclusion = rule.split(' -> ')
                premise = [p.strip() for p in premise.split(' AND ')]
                if all(p in self.knowledge_base.propositions for p in premise):
                    conclusions = [c.strip().strip('()') for c in conclusion.split(' AND ')]
                    for concl in conclusions:
                        if concl not in self.knowledge_base.propositions:
                            new_propositions.add(concl)
            if not new_propositions:
                break
            self.knowledge_base.propositions.update(new_propositions)
    
    def add_proposition(self, row, col, count):
        if count == 0:
            proposition = f"S_{row}_{col}"
        else:
            proposition = f"N_{row}_{col}_{count}"
        print("Aggiungo la proposizione: ", proposition)
        self.knowledge_base.add_proposition(proposition)
        self.moves_made.add((row,col))
        self.update_kb()

        '''# Update safe_movements and mines based on the updated knowledge base
        for prop in self.knowledge_base.propositions:
            if prop.startswith("S_"):
                _, i, j = prop.split('_')
                self.safe_movements.add((int(i), int(j)))
            elif prop.startswith("B_"):
                _, i, j = prop.split('_')
                self.mines.add((int(i), int(j)))'''
    
    def make_safe_move(self):
        if self.safe_movements:
            for movement in self.safe_movements:
                if movement not in self.moves_made:
                    self.moves_made.add(movement)
                    self.safe_movements.remove(movement)
                    return movement
        return None, None

    def make_random_move(self):
        spaces_left = (self.height * self.width) - (len(self.moves_made) + len(self.mines))
        if spaces_left == 0:
            return None
        while True:
            i = randrange(self.height)
            j = randrange(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                return i, j

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

'''# Test dell'agente e della KB
agent = Agent(6, 6)
print("REGOLE:")
for rule in agent.knowledge_base.rules[:5]:
    print(rule)
print("----------------------------")
print("Supponendo che l'utente clicca sulla cella (0,0) e trova il numero 0:")
agent.add_proposition(0, 0, 0)
for prop in agent.knowledge_base.propositions:
    print(prop)
print("-----------------------------------------------------")
print("Supponendo che l'utente clicca sulla cella (1,1) e trova il numero 2:")
agent.add_proposition(1, 1, 2)
for prop in agent.knowledge_base.propositions:
    print(prop)
'''