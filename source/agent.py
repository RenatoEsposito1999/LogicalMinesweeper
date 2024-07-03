#https://cs50.harvard.edu/extension/ai/2020/spring/projects/1/minesweeper/#:~:text=Propositional%20Logic&text=One%20way%20we%20could%20represent,a%20mine%2C%20and%20false%20otherwise.
from random import randrange
import random
import time
from cell import Cell
from sentence import Sentence
class Agent():
    """
    Thi class implement the agent that can play Minesweeper
    """
    # contains a set of all cells already clicked on
    moves_made = set()
    # contains a set of all cells known to be safe
    safes = set()
    # contains a set of all cells known to be mines
    mines = set()
    # KB that is a list of all of the Sentences that the Agent knows to be true
    knowledge_base = []

    def __init__(self, height, width):
        # Set initial height and width
        self.height = height
        self.width = width

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge_base:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge_base:
            sentence.mark_safe(cell)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper field.
        The move must be known to be safe, and not already a move
        that has been made.
        """
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            choice = random.choice(list(safe_moves))
            print(f"The agent selected a safe movement = ({choice.row},{choice.col})")
            return choice
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper field.
        """
        # Space left on the field
        spaces_left = (self.height * self.width) - (len(self.moves_made) + len(self.mines))
        
        # If no spaces return None = no movement possible
        if spaces_left == 0:
            return None
        
        while True:
            i = randrange(self.height)
            j = randrange(self.width)
            cell = Cell(i,j)
            # have not already been chosen and are not known to be mines
            if (cell not in self.moves_made) and (cell not in self.mines):
                return cell
            
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper field tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """
        # Mark the cell as a made and safe movement
        self.moves_made.add(cell)
        self.mark_safe(cell)
        #time.sleep(2)
        # Add new sentence to the Agent's KB based on the value of `cell` and `count`
        new_sentence = set()

        # Loop over adjacent cells
        for row in range(cell.row - 1, cell.row + 2):
            for col in range(cell.col - 1, cell.col + 2):
                adj_cell = Cell(row,col)
                # skip the cell itself and also when adj is know to be safe
                if (adj_cell == cell) or (adj_cell in self.safes):
                    continue
                
                # if is know that is mine the var count is decreased
                if adj_cell in self.mines:
                    print("The cell is a mine, decreasing counter.")
                    #time.sleep(2)
                    count = count - 1
                    continue
                
                # within the limits of the playing field
                # adj_cell is not in safe set and not in mines set, so we have not info on it
                # we are not sure whether adj_cell is mine or safe so they are putted in a new sentece. 
                if 0 <= row < self.height and 0 <= col < self.width:
                    #print("Non ho certezze sulla cella ",row,col," quindi diventano una nuova frase da aggiungere:")
                    #time.sleep(2)
                    new_sentence.add(adj_cell)

        # just for printing purposes
        sentence = Sentence(new_sentence, count)
        print(f'The moving on cell: ({cell.row},{cell.col}) has added sentence = {sentence} to knowledge base' )
        
        # We add the information in the form {A,B,C,D} = count i.e. among those cells there are 'count' mines, but we don't yet know which ones they are
        self.knowledge_base.append(sentence)
        # Function to infer with the new sentence mines and safe cells, and  new knowledge
        new_inference = True
        while new_inference:
            new_inference = False
            mines = set()
            safes = set()
            # We collect all the cells that we know are safe and those that are mines
            for sentence in self.knowledge_base:
                # Returns the set of all cells in each setence known to be safes.
                safes = safes.union(sentence.known_safes())
                # Returns the set of all cells in each setence known to be mines.
                mines = mines.union(sentence.known_mines())

            # If there are safe cells or mines identified, update the Knowledge Base 
            # by marking them as such and set new_inference to True to continue the loop.
            if safes:
                new_inference = True
                for safe in safes:
                    self.mark_safe(safe)
            if mines:
                new_inference = True
                for mine in mines:
                    self.mark_mine(mine)

            # Remove any empty sentences from knowledge base:
            empty = Sentence(set(), 0)
            new_knowledge = []
            for sentence in self.knowledge_base:
                if sentence != empty:
                    new_knowledge.append(sentence)
            self.knowledge_base = new_knowledge

            # Try to infer new sentences from the current ones:
            for sentence_1 in self.knowledge_base:
                for sentence_2 in self.knowledge_base:

                    # Ignore when sentences are ==
                    if sentence_1.cells == sentence_2.cells:
                        continue

                    if sentence_1.cells == Cell() and sentence_1.count > 0:
                        print('Error - sentence with no cells and count created')
                        raise ValueError

                    # Create a new sentence if 1 is subset of 2, and not in KB:
                    # ex: sentence_1: {(1, 1), (1, 2)} = 1 
                    #     sentence_2: {(1, 1), (1, 2), (1, 3)} = 2 
                    #     sentece_2 - sentece_1 = {(1,3)} = 1
                    if sentence_1.cells.issubset(sentence_2.cells):
                        new_sentence_cells = sentence_2.cells - sentence_1.cells
                        new_sentence_count = sentence_2.count - sentence_1.count

                        new_sentence = Sentence(new_sentence_cells, new_sentence_count)

                        # Add to knowledge if not already in KB:
                        if new_sentence not in self.knowledge_base:
                            new_inference = True
                            print('New Inferred Knowledge: ', new_sentence, 'from', sentence_1, ' and ', sentence_2)
                            self.knowledge_base.append(new_sentence)

        # Print out AI current knowledge to terminal:
        print('Current AI KB length: ',len(self.knowledge_base))
        mines = Sentence(self.mines,len(self.mines))
        print('Known Mines: ', mines)
        remaining = Sentence(self.safes-self.moves_made,len(self.safes-self.moves_made))
        print('Safe Moves Remaining: ', remaining)
        print('====================================================')
