import random
from cell import Cell
# It is a representation of the game - Manages the game
class Minesweeper():
    def __init__(self, height, width, mines):
        self.height = height
        self.width = width
        # This set represents the locations of the cells that have mines.
        # Is used, with the mines_found set, to check the victory
        self.mines = set()
        # No mines found
        self.mines_found = set()
        # Empty field
        self.field = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Cell(i,j))
            self.field.append(row)
        # Add mines randomly
        count = 0
        while count != mines:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            #check each cell
            if not self.field[i][j].get_has_mine():
                self.mines.add(Cell(i, j))
                self.field[i][j].set_has_mine(True)
                count+=1
                #self.field[i][j] = True
        
        # Added the number of nearby mines.
        self.compute_nearby_mines()
        self.print()

    def get_cell_from_field(self,cell):
        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j] == cell:
                    return self.field[i][j]
        return None

    def print(self):
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.field[i][j].get_has_mine():
                    print("|X", end="")
                else:
                    print(f"|{self.field[i][j].get_number()}", end="")
            print("|")
        print("--" * self.width + "-")
        string = "Mines are in: "
        for cell in self.mines:
            string+=f"({cell.get_row()},{cell.get_col()})"
        print(string)

    def is_mine(self,cell):
        return self.get_cell_from_field(cell).get_has_mine()

    def compute_nearby_mines(self):
        # Keep count of nearby mines
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),         (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for row in range(len(self.field)):
            for col in range(len(self.field[0])):
                if self.field[row][col].get_has_mine():
                    continue
                mine_count = 0
                for dr, dc in directions:
                    r, c = row + dr, col + dc
                    if 0 <= r < len(self.field) and 0 <= c < len(self.field[0]):
                        if self.field[r][c].get_has_mine():
                            mine_count += 1
                self.field[row][col].set_number(mine_count)

    def get_nearby_mines(self, cell):
        '''Returns the number of nearby mines of a given cell'''
        return self.get_cell_from_field(cell).number

    def won(self):
        #Checks if all mines have been flagged.
        return self.mines_found == self.mines
    
    
