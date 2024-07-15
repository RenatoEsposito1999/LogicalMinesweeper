import pygame
import sys
import time

from cell import Cell
from minesweeper import Minesweeper
from agent import Agent

HEIGHT = 6
WIDTH = 6
MINES = 6

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Create game
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

first_move = True

# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = Agent(height=HEIGHT, width=WIDTH)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False
win = False
# Show instructions initially
instructions = True
while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)
    
    # Show game instructions
    if instructions:
        
        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Play game button
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        # Rules
        rules = [
        "Click on 'Next move' to allow the agent to move",
        "Mark all mines successfully to win!"
    ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        pygame.display.flip()
        continue
    
    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)
            cell = Cell(i,j)
            # Add a mine, flag, or number if needed
            if game.is_mine(cell) and lost:
                screen.blit(mine, rect)
            elif cell in flags:
                screen.blit(flag, rect)
            elif cell in revealed:
                neighbors = smallFont.render(
                    str(game.get_nearby_mines(cell)),
                    True, BLACK
                )
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)

            row.append(rect)
        cells.append(row)

    # AI Move button
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("AI Move", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = aiButton.center
    pygame.draw.rect(screen, WHITE, aiButton)
    screen.blit(buttonText, buttonRect)

    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Reset", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(buttonText, buttonRect)
   

    # Display text
    if game.mines == flags:
        text = 'Won'
        win = True
        # Automatically show the remaining cells
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if (Cell(i,j) not in revealed) and Cell(i,j) not in flags:
                    revealed.add(Cell(i,j)) 
    elif lost:
        text = 'Lost'
    else:
        text = ""
    #text = "Lost" if lost else "Won" if game.mines == flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, (2 / 3) * height)
    screen.blit(text, textRect)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    '''# Check for a right-click to toggle flagging
    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (Cell(i, j) not in revealed):
                    if (Cell(i, j) in flags):
                        flags.remove(Cell(i, j))
                    else:
                        flags.add(Cell(i, j))
                    time.sleep(0.2)
'''
    #elif left == 1:
    if left == 1: 
        mouse = pygame.mouse.get_pos()

        # If AI button clicked, make an AI move
        if aiButton.collidepoint(mouse) and not lost and not win:
            move = ai.make_safe_move()
            if move is None: # means no safe move
                move = ai.make_random_move()
                if move:
                    #First move must be always safe.
                    while first_move:
                        if game.is_mine(move):
                            move = ai.make_random_move()
                        else:
                            first_move = False
                    print(f"[Agent] Select a random element --> ({move.row},{move.col})")
                else: #means NO RANDOM MOVE possibile due lack of space = VICTORY
                    flags = ai.mines.copy()
                    print("No moves left to make.")
            else:
                print("AI making safe move.")
            time.sleep(0.2)

        # Reset game state
        elif resetButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = Agent(height=HEIGHT, width=WIDTH)
            win = False
            revealed = set()
            flags = set()
            lost = False
            first_move = True
            move = None
            continue

        '''# User-made move
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and Cell(i, j) not in flags
                            and Cell(i, j) not in revealed):
                        move = Cell(i, j)'''
        
    # Make move and update AI knowledge
    if move:
        if game.is_mine(move):
            lost = True
        else:
            nearby = game.get_nearby_mines(move)
            if nearby is not None:
                revealed.add(move)
                #ai.add_knowledge(move, game.get_nearby_mines(move))
                bombs = ai.add_knowledge(move, nearby)
                # To flag the found bombs
                if bombs:
                    for b in bombs:
                        if b not in flags:
                            flags.add(b)
            else:
                print("[ERROR]: No cell corresponds to the chosen movement")

    pygame.display.flip()
