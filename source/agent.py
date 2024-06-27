import re
from knowledge import KnowledgeBase
class Agent():

    def __init__(self) -> None:
        self.knowledge_base = KnowledgeBase()
    
    '''
        Questa versione di update_kb non è completamente iterativa. Dovrebbe essere migliorata per assicurarsi che 
        tutte le possibili nuove informazioni vengano trovate iterativamente, 
        poiché alcune nuove proposizioni possono attivare ulteriori regole che a loro volta possono generare ancora più nuove proposizioni.
    '''

    '''def update_kb(self):
        new_propositions = set()
        for rule in self.knowledge_base.rules:
            premise, conclusion = rule.split(' -> ')
            if all(p in self.knowledge_base.propositions for p in premise.split(' AND ')):
                conclusions = conclusion.split(' AND ')
                new_propositions.update(conclusions)
        self.knowledge_base.propositions.update(new_propositions)'''
    '''Qui l'agente sa solamente ritornare quello che trova in i j n e k(se c'è)'''

    ''' Questa versione è migliore di prima, perché qui 
        Inizializzazione: La KB viene inizializzata con le proposizioni conosciute.
        Ciclo Iterativo: Nel metodo update_kb, un ciclo while True continua finché ci sono nuove proposizioni da aggiungere.
        Applicazione delle Regole: Per ogni regola, se le premesse della regola sono soddisfatte dalle proposizioni attuali nella KB, le conclusioni della regola vengono aggiunte a un set di nuove proposizioni.
        Aggiornamento delle Proposizioni: Se non ci sono nuove proposizioni da aggiungere (added_propositions è vuoto), il ciclo si interrompe. Altrimenti, le nuove proposizioni vengono aggiunte alla KB e il ciclo continua.
        Conclusione: Quando il ciclo termina, tutte le possibili inferenze sono state aggiunte alla KB.
        '''
    
    def update_kb(self):
        new_propositions = set(self.knowledge_base.propositions)
        while True:
            added_propositions = set()
            for rule in self.knowledge_base.rules:
                premise, conclusion = rule.split(' -> ')
                if all(p in new_propositions for p in premise.split(' AND ')):
                    conclusions = conclusion.split(' AND ')
                    for concl in conclusions:
                        if concl not in new_propositions:
                            added_propositions.add(concl)
            if not added_propositions:
                break
            new_propositions.update(added_propositions)
        self.knowledge_base.propositions = new_propositions
    

    def add_proposition(self, proposition):
        self.knowledge_base.add_proposition(proposition)
        self.update_kb()

    def estrai_valori_da_stringa(s):
        # Definisci un pattern regex per cercare il formato N_{i}_{j}_{k}
        pattern = r"N_(\d+)_(\d+)(?:_(\d+))?"
        
        # Cerca il pattern nella stringa di input
        match = re.search(pattern, s)
        
        if match:
            # Estrai i valori dai gruppi corrispondenti
            N = int(match.group(1))
            i = int(match.group(2))
            k = int(match.group(3)) if match.group(3) else None
            return N, i, k
        else:
            return None

    '''# Esempio di utilizzo
    stringa_input = "N_42_10"
    risultato = estrai_valori_da_stringa(stringa_input)
    if risultato:
        N, i, k = risultato
        print(f"N: {N}, i: {i}, k: {k if k is not None else 'non presente'}")
    else:
        print("Pattern non trovato nella stringa di input.")'''
agent = Agent()
print("REGOLE")
for rule in agent.knowledge_base.rules[:5]:
    print(rule)
print("----------------------------")
print("Supponendo che l'utente clicca sulla cella 0,0 e trova il numero 0 allora scopre:")
agent.add_proposition("N_0_0_0")
print(len(agent.knowledge_base.propositions))
for rule in agent.knowledge_base.propositions:
    print(rule)
print("-----------------------------------------------------")
agent.add_proposition("N_1_1_2")
print(len(agent.knowledge_base.propositions))
for rule in agent.knowledge_base.propositions:
    print(rule)

