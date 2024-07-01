import random
import sys
import time
import os
from cell import Cell
from minesweeper import Minesweeper
from agent import Agent


def print_field(field,height,width):
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(height):
            print("--" * width + "-")
            for j in range(width):
                if not field[i][j].unknow:
                    '''if field[i][j].get_has_mine():
                        print("|X", end="")
                    else:'''
                    print(f"|{field[i][j].get_number()}", end="")
                else:
                    print("|U",end="")
            print("|")
        print("--" * width + "-")
        


HEIGHT = 6
WIDTH = 6
MINES = 6
first_move = True
lost = False
revealed = set()
flags = set()
# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = Agent(height=HEIGHT, width=WIDTH,n_mines=MINES)


tmp_field = []
for i in range(HEIGHT):
    row = []
    for j in range(WIDTH):
        row.append(Cell(i,j))
    tmp_field.append(row)

while not lost:
    print_field(tmp_field,HEIGHT,WIDTH)
    print(random.randint(0,10))
    input("Press Enter to continue...")
    


'''
# Empty field
        self.field = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Cell(i,j))
            self.field.append(row)'''


