import pygame
import random
import settings as st
from minesweeper_logical import LogicalMinesweeper
class MinesweeperUI:
    # List of tuples, where each one is a pair: rectangle, id
    grid_rects = []
    first_move = True
    def __init__(self) -> None:
        pygame.init()
        # Window creation
        self.window = pygame.display.set_mode((st.WINDOW_WIDTH, st.WINDOW_HEIGHT))
        pygame.display.set_caption('Minesweeper')
        # Fonts for text
        self.font = pygame.font.Font(None, 36)

        self.next_button = self.draw_button(st.button_y1,"Start game")
        self.reset_button = self.draw_button(st.button_y2,"Reset")
        self.draw_grid()
        
        # Refreshing the window
        pygame.display.flip()
        # Main loop of the game
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = event.pos
                        for rect, rect_id in self.grid_rects:
                            if rect.collidepoint(mouse_pos):
                                print(f"Clicked on rectangle ID: {rect_id}")
                                break
                        if self.next_button.collidepoint(mouse_pos):
                            if self.first_move:
                                self.next_button = self.draw_button(st.button_y1, "Next move")
                                safe_row = random.randint(0,5)
                                safe_col = random.randint(0, 5)
                                self.logical_minesweeper = LogicalMinesweeper(self, safe_row,safe_col)
                                self.first_move = False
                            else:
                                print("Next move")
                        if self.reset_button.collidepoint(mouse_pos):
                            print("Reset")
                # IF TASTO DESTRO METTI BANDIERA
            pygame.display.flip()


    ''' 
    Implementare il reset
    Ora devo implementare la logica proposizionale
    Aggiornare i rettangoli della griglia so già farlo,  Capire come far comunicare le informazioni grafiche.
    Capire come far comunicare le informazioni grafiche.
    '''


    def draw_grid(self):
        for row in range(st.GRID_SIZE):
            for col in range(st.GRID_SIZE):
                rect = pygame.Rect(
                    st.grid_x + col * (st.CELL_SIZE + st.GRID_PADDING),
                    st.grid_y + row * (st.CELL_SIZE + st.GRID_PADDING),
                    st.CELL_SIZE,
                    st.CELL_SIZE
                )
                self.grid_rects.append((rect, row * st.GRID_SIZE + col))
                pygame.draw.rect(self.window, st.GRID_COLOR, rect)
                pygame.draw.rect(self.window, st.BORDER_COLOR, rect, 2)

    def draw_button(self, y, text):
        rect = pygame.Rect(st.button_x, y, st.BUTTON_WIDTH, st.BUTTON_HEIGHT)
        pygame.draw.rect(self.window, st.BUTTON_COLOR, rect)
        pygame.draw.rect(self.window, st.BORDER_COLOR, rect, 2)
        text_surf = self.font.render(text, True, st.TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        self.window.blit(text_surf, text_rect)
        return rect

