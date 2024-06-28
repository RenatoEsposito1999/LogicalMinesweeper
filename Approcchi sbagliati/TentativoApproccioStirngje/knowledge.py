from itertools import combinations
from random import randrange
import re

class KnowledgeBase:
    def __init__(self, height, width):
        self.propositions = set()
        self.height = height
        self.width = width
        self.rules = self.generate_rules()
    
    def add_proposition(self, proposition):
        self.propositions.add(proposition)
    
    def generate_rules(self):
        rules = []
        for i in range(self.height):
            for j in range(self.width):
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
                    comb_rules = ' OR '.join([' AND '.join([f"B_{x}_{y}" if (x, y) in c else f"NOT B_{x}_{y}" for x, y in adj]) for c in comb])
                    rules.append(f"N_{i}_{j}_{k} -> ({comb_rules})")
        return rules
    
    def adjacent_cells(self, i, j):
        adj = []
        for x in range(max(0, i-1), min(self.height, i+2)):
            for y in range(max(0, j-1), min(self.width, j+2)):
                if (x, y) != (i, j):
                    adj.append((x, y))
        return adj

    def combinations(self, elements, k):
        return list(combinations(elements, k))

    def __str__(self):
        return f"Knowledge Base: {self.propositions}"
