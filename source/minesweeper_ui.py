import pygame
from minesweeper_logical import LogicalMinesweeper
class MinesweeperUI:
    WIDTH = 800
    HEIGHT = 800
    TITLE = "Logical Minesweeper"
    def __init__(self):
        # QUESTA ISTANZIAZIONE ANDEREBBE FATTA AL PRIMO CLICK, perché il primo click è sempre 0.   
        #self.logical_minesweeper = LogicalMinesweeper()
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        pygame.display.set_caption(self.TITLE)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Aggiorna il display
            pygame.display.flip()


        # END WHILE
        