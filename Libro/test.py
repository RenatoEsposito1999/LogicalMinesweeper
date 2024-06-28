
from library.utils import *
from library.logic import *
from generazioneclausole import *
#(x, y, P, Q, f) = symbols('x, y, P, Q, f')
#sentece = P & ~Q
#print(sentece.op)
#print(sentece.args)
#sentence = expr('~(P & Q)  ==>  (~P | ~Q)')
#print(sentence)


'''wumpus_kb = PropKB()
P11, P12, P21, P22, P31, B11, B21 = expr('P11, P12, P21, P22, P31, B11, B21')
wumpus_kb.tell(~P11)
wumpus_kb.tell(B11 | '<=>' | ((P12 | P21)))
wumpus_kb.tell(B21 | '<=>' | ((P11 | P22 | P31)))
wumpus_kb.tell(~B11)
wumpus_kb.tell(B21)
#for clauses in wumpus_kb.clauses:
#    print(clauses)
print(wumpus_kb.ask_if_true(~P11))
'''
'''clauses = ['(B & F)==>E', 
           '(A & E & F)==>G', 
           '(B & C)==>F', 
           '(A & B)==>D', 
           '(E & F)==>H', 
           '(H & I)==>J',
           'A', 
           'B', 
           'C']'''
'''clauses = ['(B & F)==>E', 
           '(A & E & F)==>G', 
           '(B & C)==>F', 
           '(A & B)==>D', 
           '(E & F)==>H', 
           '(H & I)==>J',
           'G==>O',
           'A', 
           'B', 
           'C']'''
'''definite_clauses_KB = PropDefiniteKB()
for clause in clauses:
    definite_clauses_KB.tell(expr(clause))
print("# DOPO LA TELL, KB entails O?")
print(pl_fc_entails(definite_clauses_KB, expr('O')))
print("# DOPO LA TELL, KB entails G?")
print(pl_fc_entails(definite_clauses_KB, expr('G')))
if (pl_fc_entails(definite_clauses_KB, expr('G'))):
    definite_clauses_KB.tell(expr('G'))
print("# DOPO LA TELL, KB entails O?")
print(pl_fc_entails(definite_clauses_KB, expr('O')))
for cl in definite_clauses_KB.clauses:
    print(cl)'''
'''print(pl_fc_entails(definite_clauses_KB, expr('H')))
print(pl_fc_entails(definite_clauses_KB, expr('I')))
print(pl_fc_entails(definite_clauses_KB, expr('j')))'''

'''clauses = [
    'S_0_1 & S_1_0 & S_1_1 ==> N_0_0_0',
]'''
kb = PropDefiniteKB()
for clause in clauses:
    kb.tell(expr(clause))
kb.tell(expr('N_0_0_0'))
print(pl_fc_entails(kb,expr('S_0_1')))

