from math import floor
import settings as st
import random
# LE FUNZIONI LE POSSO NOMINARE IN MANIERA TUTTE PICCOLE E CON _ PER SPERARE NOMI
# Le variabili devono essere descrittive lower case e separate da _ 
# I nomi dei moduli devono essere tutti piccoli e separati da _ 
# le costanti upper case.
class LogicalMinesweeper:
    def __init__(self):
        # Initialization of the logical field
        self.field = []
        # field is a list of lists, each list is a row of the filed, each element of this rows 
        for row in range(st.N_ROWS):
            new_row = []
            for col in range(st.N_COLS):
                new_row.append(0)
            self.field.append(new_row)
         # LIST COMPRESSION --> field = [[0 for _ in range(self.N_COLS)] for _ in range(self.N_ROWS)]
        '''
        field = [
    [0, 0, 0, 0, 0, 0],  # Prima riga
    [0, 0, 0, 0, 0, 0],  # Seconda riga
    [0, 0, 0, 0, 0, 0],  # Terza riga
    [0, 0, 0, 0, 0, 0],  # Quarta riga
    [0, 0, 0, 0, 0, 0],  # Quinta riga
    [0, 0, 0, 0, 0, 0]   # Sesta riga
    ]
    '''

        # Posizionamento delle mine
        mines_placed = 0
        while mines_placed < st.N_MINES:
            row = random.randint(0, st.N_ROWS - 1)
            col = random.randint(0, st.N_COLS - 1)
            if self.field[row][col] != -1:
                self.field[row][col] = -1
                mines_placed += 1

        # Calcolo del numero di mine adiacenti per ogni cella
        for row in range(st.N_ROWS):
            for col in range(st.N_COLS):
                if self.field[row][col] == -1:
                    continue
                count = 0
                for i in range(max(0, row - 1), min(st.N_ROWS, row + 2)):
                    for j in range(max(0, col - 1), min(st.N_COLS, col + 2)):
                        if self.field[i][j] == -1:
                            count += 1
                self.field[row][col] = count

        # Stampa del campo (solo per scopi di debug)
        for row in self.field:
            print(" ".join(str(cell) if cell != -1 else "*" for cell in row))


        
        

    