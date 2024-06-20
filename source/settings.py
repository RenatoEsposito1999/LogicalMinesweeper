
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
GRID_SIZE = 6
CELL_SIZE = 60
GRID_PADDING = 2
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20
GRID_COLOR = (169, 169, 169)  # Grey
BORDER_COLOR = (255, 255, 255)  # WHITE
TEXT_COLOR = (0, 0, 0)  # Nero
BUTTON_COLOR = (200, 200, 200)  # Light grey
# Calculation of positions
grid_width = GRID_SIZE * (CELL_SIZE + GRID_PADDING)
grid_height = GRID_SIZE * (CELL_SIZE +GRID_PADDING)
grid_x = (WINDOW_WIDTH - grid_width - BUTTON_WIDTH) // 2
grid_y = (WINDOW_HEIGHT - grid_height) // 2
button_x = grid_x + grid_width + BUTTON_MARGIN
total_button_height = BUTTON_HEIGHT * 2 + BUTTON_MARGIN
button_start_y = (WINDOW_HEIGHT - total_button_height) // 2
button_y1 = button_start_y
button_y2 = button_y1 + BUTTON_HEIGHT + BUTTON_MARGIN