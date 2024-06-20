import pygame
import settings as st
class MinesweeperUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((st.WIDTH, st.HEIGHT))
        pygame.display.set_caption(st.TITLE)
        self.clock = pygame.time.Clock()
        self.screen.fill(st.BLACK)
        self.font = pygame.font.SysFont(None, 40)


        self.draw_grid()
        self.draw_buttons()
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row, col = y // st.CELL_SIZE, x // st.CELL_SIZE
                    '''if not self.logical_minesweeper:
                        self.logical_minesweeper = LogicalMinesweeper(20, 20, 40)
                        # Assicurati che il primo click non sia su una mina
                        while self.logical_minesweeper.grid[row][col] == -1:
                            self.logical_minesweeper = LogicalMinesweeper(20, 20, 40)
                    self.logical_minesweeper.reveal(row, col)'''
            

        pygame.quit()

    def draw_grid(self):
        for x in range(0, st.GRID_WIDTH, st.CELL_SIZE):
            for y in range(0, st.HEIGHT, st.CELL_SIZE):
                rect = pygame.Rect(x, y, st.CELL_SIZE, st.CELL_SIZE)
                pygame.draw.rect(self.screen, st.GRAY, rect, 1)
    
    def draw_buttons(self):
        text1 = self.font.render("Next move", True, st.WHITE)
        text_rect = text1.get_rect()
        #button_next_move = pygame.Rect(st.GRID_WIDTH + 50, 100, 100, 50)
        button_next_move = pygame.Rect(st.GRID_WIDTH + 50, 100, 100, 50)
        pygame.draw.rect(self.screen, st.LIGHT, button_next_move)


        self.screen.blit(text1, (st.GRID_WIDTH + 60, 110))
