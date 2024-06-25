from cell import Cell
class Sentence():
    '''
    This class represent logical sentences if the form {cell_A,cell_B,cell_C,cell_D} = 3, this means that in this four cells there are 3 mines. 
    A sentence consists of a set of cells, and a count of the number of those cells which are mines.
    '''
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        '''Override of == '''
        if isinstance(other, Sentence):
            return self.cells == other.cells and self.count == other.count
        return False
    
    def __str__(self):
        '''Override for str(sentence)'''
        empty = "{"
        empty += ",".join(f"({cell.row},{cell.col})" for cell in self.cells)
        empty += "}"
        empty += f" = {self.count}"
        return empty

    def known_mines(self):
        '''
        Returns the set of all cells in self.cells known to be mines.
        '''
        if len(self.cells) == self.count and self.count != 0:
            # means that all the cells are mines
            print('Mine Identified! - ', self.cells)
            return self.cells
        else:
            # we cannot determine which specific cells are mines, so return an empty set
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            # if is 0 means that all the cells in the sentence are SAFE
            return self.cells
        else:
            # means that there are cells containing mines, but we don't know which ones so we return an empty set
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If the cell is present in self.cells, it is removed from the set. Removing the cell from the set means that it will no longer be considered in the knowledge representation of this sentence.
        # this means that one of the cells thought to be a mine was confirmed as such, so the number of unknown mines in the sentence is reduced by one.
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=1
        # after this if for example we  call know_safes and returns a non empty set we know that all cells in the set are safe. 

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        raise NotImplementedError
'''
# Creazione dei set di celle
new_sentence_cells = set()
new_sentence_cells.add(Cell(0, 1))
new_sentence_cells.add(Cell(1, 1))
new_sentence_cells.add(Cell(1, 3))

# Creazione dell'oggetto Sentence
test = Sentence(new_sentence_cells, 3)

# Creazione di un altro set di celle
new_sentence_cells = set()
new_sentence_cells.add(Cell(1, 3))
new_sentence_cells.add(Cell(1, 1))
new_sentence_cells.add(Cell(0, 1))

# Creazione di un altro oggetto Sentence
test2 = Sentence(new_sentence_cells, 3)

# Verifica di uguaglianza
print(str(test))
'''
# Esempio di celle
cells = {Cell(0, 1), Cell(1, 1), Cell(1, 3)}

# Creazione di un oggetto Sentence con count=3
sentence = Sentence(cells, 1)

# Marking a cell as a mine
mine_cell = Cell(1, 1)
sentence.mark_mine(mine_cell)

# Output dello stato aggiornato
print(f"Cells: {str(sentence)}")  # Questo mostrerà le celle rimanenti
print(f"Count: {sentence.count}")  # Questo mostrerà il conteggio aggiornato delle mine
if sentence.known_safes():
    print("TUTTO SICURO")