import pygame
import settings as st

class MinesweeperUI:
    # List of tuples, where each one is a pair: rectangle, id
    grid_rects = []
    def __init__(self) -> None:
        pygame.init()
        # Window creation
        self.window = pygame.display.set_mode((st.WINDOW_WIDTH, st.WINDOW_HEIGHT))
        pygame.display.set_caption('Minesweeper')
        # Fonts for text
        self.font = pygame.font.Font(None, 36)

        self.next_button = self.draw_button(st.button_y1,"Next move")
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
                            print("Next move")
                        if self.reset_button.collidepoint(mouse_pos):
                            print("Reset")
                # IF TASTO DESTRO METTI BANDIERA

    '''
    Posso iniziare a fare il primo step cioè l'utente clicca next move e poiché c'è un flag che indica che qualsais è sicuro allora possiamo scoprire celle e quindi inizializzare il campo. 
    Posso decidere empiricamente che il primo click è sicuramente vuoto o posso anche non farlo, ma nelle slide l'ho scritto. 
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

