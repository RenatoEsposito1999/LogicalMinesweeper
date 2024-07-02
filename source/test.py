import os
import sys
from cell import Cell
from minesweeper import Minesweeper
from agent import Agent


HEIGHT = 4
WIDTH = 4
MINES = 4
first_move = True
lost = False
revealed = set()
flags = set()
# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = Agent(height=HEIGHT, width=WIDTH,n_mines=MINES)

def print_field(field,height,width):
        #os.system('cls' if os.name == 'nt' else 'clear')
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
        

tmp_field = []
for i in range(HEIGHT):
    row = []
    for j in range(WIDTH):
        row.append(Cell(i,j))
    tmp_field.append(row)
print("Field of the agent")
print_field(tmp_field,HEIGHT,WIDTH)

while not lost:
    print("Press ENTER to continue...")
    print("Write ESC to exit.")
    print("Press R to reset.")
    print("Enter a pair of numbers separated by a space to indicate a possible cell containing a bomb (e.g. '3 5').")

    user_input = input("Waiting for input: ")
    if user_input == "":
        os.system('cls||clear')
        i,j = ai.make_safe_move()
        if (i is None) or (j is None): # means no safe move
            i,j = ai.make_random_move()
            move = Cell(i,j)
            if move: # it's possible to make random movement
                while first_move: #First move must be always safe.
                    if game.is_mine(move):
                        i,j = ai.make_random_move()
                        move = Cell(i,j)
                    else:
                        first_move = False
                print(f"[Agent] Select a random element --> ({move.row},{move.col})\nValue found {game.field[move.row][move.col].get_number()}")
            else: #means NO RANDOM MOVE possibile due lack of space = VICTORY
                print("No moves left to make.")
        else:
            move = Cell(i,j)
            print(f"AI making safe move --> ({i},{j})\nValue found: {game.field[i][j].get_number()}")

        # Make move and update AI knowledge
        if move:
            if game.is_mine(move):
                lost = True
                print("LOST!")
                sys.exit()
            else:
                nearby = game.get_nearby_mines(move)
                #revealed.add(move)
                tmp_field[move.row][move.col].unknow = False
                tmp_field[move.row][move.col].set_number(nearby)
                ai.add_knowledge(move.row,move.col,nearby)
                print_field(tmp_field,HEIGHT,WIDTH)
    elif user_input.lower() == "esc":
        sys.exit()
    elif user_input.lower() == "r":
        print("Reset del gioco.")
    else:
        try:
            x, y = map(int, user_input.split())
            print(f"Hai inserito le coordinate: ({x}, {y})")
            #QUesto è per "mettere una bandiera"
        except ValueError:
            print("Input non valido. Inserisci una coppia di numeri separati da uno spazio.")

    

'''
# Empty field
        self.field = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Cell(i,j))
            self.field.append(row)'''

