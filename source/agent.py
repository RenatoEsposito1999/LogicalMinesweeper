#https://cs50.harvard.edu/extension/ai/2020/spring/projects/1/minesweeper/#:~:text=Propositional%20Logic&text=One%20way%20we%20could%20represent,a%20mine%2C%20and%20false%20otherwise.
from random import randrange
import random
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

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper field tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        raise NotImplementedError

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
                print(f"The agent selected a movement at random: ({cell.row},{cell.col})")
                return cell
            
    
test = Agent(6,6)
test.safes.add(Cell(0,0))
test.safes.add(Cell(1,0))
test.safes.add(Cell(2,0))
test.safes.add(Cell(3,0))
test.make_safe_move()


