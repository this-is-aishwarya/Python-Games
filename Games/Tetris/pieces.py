import pygame
import random

pygame.font.init()

# GLOBAL VARIABLES
w_height = 800
w_width = 700
play_width = 300
play_height = 600

background = pygame.image.load("background.jpg")
block_size = 30

top_left_x = (w_width - play_width) // 2
top_left_y = w_height - play_height


# SHAPE ORIENTATION

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '...0.',
      '...0.',
      '..00.',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '..00.',
      '...0.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....']]

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

T = [['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '...0.',
      '..00.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....']]
A= [['.....',
      '..0..',
      '.000.',
      '..0..',
      '.....']]
U = [['.....',
      '.0.0.',
      '.0.0.',
      '.000.',
      '.....'],
     ['.....',
      '.000.',
      '.0...',
      '.000.',
      '.....'],
     ['.....',
      '.000.',
      '.0.0.',
      '.0.0.',
      '.....'],
     ['.....',
      '.000.',
      '...0.',
      '.000.',
      '.....']
     ]
# GLOBAL VARIABLES

shapes = [S, Z, I, O, J, L, T,A,U]
shape_colors = [(0, 255, 0), (102,0,51), (255,229,204),(255, 0, 0), (0, 255, 255), (255, 255, 0), (255,128,0),(255, 165, 0), (128, 0, 128),(225,0,165),(165,89,230)]
score=0
# CLASS DEFINITION

class Piece:
    x = 10  # Number of columns
    y = 20  # Number of rows,
    shape = 0  # Shape of piece, set default to 0
    color = ()  # Color of shape
    rotation = 0  # Current orientation/rotation, default set to 0

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = random.choice(shape_colors)
        self.rotation = 0


# FUNCTION DEFINITIONS

def draw_text_middle(text, size, color, surface):
    # Which font do you want to use?
    font = pygame.font.SysFont('comicsans', size, bold=True)
    # Render the Text using font
    label = font.render(text, 1, color)
    # Print the Text using label
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def create_grid(locked_positions={}):
    # Create a 10*20 matrix initialized with (0,0,0)
    grid = [[(0, 0, 0) for x in range(10)] for y in range(20)]
    # Color the grid where the blocks are occupied already
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def check_lost(positions):
  # Traverse through the locked positions
    for pos in positions:
        x, y = pos
        # If block crosses the above boundary of grid
        if y < 1:
            return True
    return False

def get_shape():
    # Make a new object of type Piece with a randomly chosen shape
    newPiece = Piece(5, 0, random.choice(shapes))
    # return this object
    return newPiece


def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    # Loop over the formatted grid
    i = 0
    for line in format:
        row = list(line)
        j = 0
        for column in row:
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
            j += 1
        i += 1
    k = 0
    for pos in positions:
        positions[k] = (pos[0] - 2, pos[1] - 4)
        k += 1
    return positions


def valid_space(piece, grid):
    # Matrix of all positions which are not currently occupied
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # Narrow down the matrix for easier handling
    accepted_positions = [j for sub in accepted_positions for j in sub]
    # convert_shape_format returns a list of strings of the current shape in its correct orientation
    formatted = convert_shape_format(piece)
    # Check if the block lies in a position that is not accepted (not valid)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def draw_next_shape(piece, surface):
    # Decide the font and render it
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    # Where to display the next piece? These are the coordinates
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    # List of strings depicting the orientation of piece
    format = piece.shape[piece.rotation % len(piece.shape)]
    i = 0
    for line in format:
      row = list(line)
      j = 0
      # Traverse through each string
      for column in row:
        if column == '0':
          # Draw the next_piece
          pygame.draw.rect(surface, piece.color, (sx + j * 30, sy + i * 30, 30, 30), 0)
        j += 1
      i += 1
    surface.blit(label, (sx + 10, sy - 30))
    update_score(surface)

def update_score(surface):
    # Same as draw_text_middle, except that we decide the position to print
    # Decide the font, render it on the text and print it on the surface
    text = "Score : " + str(score)
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render(text, 1, (255,255,255))
    sx = top_left_x + play_width + 40
    sy = top_left_y + play_height/2 - 100
    surface.blit(label, (sx + 10, sy+ 150))

def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        # Draw Horizontal Lines
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * 30), (sx + play_width, sy + i * 30))
        for j in range(col):
              # Draw Vertical Lines
              pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))


def draw_window(surface):
  # Fill the window with Black Color
  surface.fill((0, 0, 0))
  # We did this in the draw_text_middle() function
  # Decide the font, render the text with font, and print it on surface
  font = pygame.font.SysFont('comicsans', 60)
  label = font.render('TETRIS', 1, (255, 255, 255))
  surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
  # Draw the current_piece in grid
  # Traverse through the entire grid
  for i in range(len(grid)):
    for j in range(len(grid[i])):
        # draw the block
        pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, block_size, block_size), 0)

  draw_grid(surface, 20, 10)
  pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)


def clear_rows(grid, locked):
    global score
    # We store the number of rows to shift down in inc
    inc = 0
    # Traverse the grid in reverse direction
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        # Check if there is any empty position(block) in this row
        if (0, 0, 0) not in row:
            inc +=1
            # Clear this row, save the index into ind
            ind = i
            for j in range(len(row)):
                try:
                    del locked[ (j, i) ]
                except:
                    continue

    # Shift the remaining rows downward by inc number of rows
    if inc > 0:
        # Sort the locked position, store into temp
        temp = sorted(list(locked), key=lambda x: x[1])
        # Traverse temp in reverse direction
        for key in temp[::-1]:
            x, y = key
            # If the y coordinate of this position is less than ind
            if y < ind:
                # Update the y coordinate
                newKey = (x, y + inc)
                # Remove the previous locked position from the list
                locked[newKey] = locked.pop(key)
        score+=10

def play():
    # A global variable grid
    global grid
    # The positions already occupied
    locked_positions = {}
    # create_grid returns the created grid
    grid = create_grid(locked_positions)

    # change_piece turns True when the next piece is to be released
    change_piece = False
    # run remains True unless the user decides to quit
    run = True
    # current_piece holds the current piece falling in the grid
    current_piece = get_shape()
    # next_piece holds the piece that would fall once the current one sets down
    next_piece = get_shape()
    # clock is used to keep a track of time for the falling piece
    clock = pygame.time.Clock()
    # This keeps a track of the time to automatically move
    # current_piece one position down in vertical direction
    fall_time = 0

    while run:
        # Decide the falling speed
        fall_speed = 0.27
        # An updated grid is created each time
        grid = create_grid(locked_positions)
        # update the fall_time
        fall_time += clock.get_rawtime()
        # Move the clock ahead
        clock.tick()

        # This block decides when to move the piece down
        # vertically by one position
        if fall_time / 1000 >= fall_speed:
            # Update the clock time and piece position
            fall_time = 0
            current_piece.y += 1
            # Check if the piece touches the ground or existing stack
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
              if event.type == pygame.QUIT:
                run = False
                # Simply quit the game window
                pygame.display.quit()
                # Exit the game now
                quit()

              if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                  current_piece.x -= 1
                  if not valid_space(current_piece, grid):
                    current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                  current_piece.x += 1
                  if not valid_space(current_piece, grid):
                    current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                  current_piece.y += 1
                  if not valid_space(current_piece, grid):
                    current_piece.y -= 1

                elif event.key == pygame.K_UP:
                  current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                  if not valid_space(current_piece, grid):
                     current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

          # Convert the current_position into coordinates on the grid
        shape_pos = convert_shape_format(current_piece)
        # Traverse through the grid and color it!
        for i in range(len(shape_pos)):
               x, y = shape_pos[i]
               if y > -1:
                  grid[y][x] = current_piece.color

          # If change_piece is true, update the locked_positions by the current_piece
        if change_piece:
             for pos in shape_pos:
                  p = (pos[0], pos[1])
                  locked_positions[p] = current_piece.color
              # Then, assign next_piece to current_piece, assign random shape to next_piece
             current_piece = next_piece
             next_piece = get_shape()
             # Revert change_piece to False for the next falling piece
             change_piece = False
             clear_rows(grid, locked_positions)

        draw_window(window)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        # Check if no space on grid
        if check_lost(locked_positions):
           run = False


    window.fill((0, 0, 0))
    draw_text_middle("You Lost", 80, (255, 255, 255), window)
    # Update the screen
    pygame.display.update()
    pygame.time.delay(2000)

def game():
    run = True
    # Our game runs until 'run' is made 'False'
    while run:
        # Fill the window with Black Colour (RGB Value)
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))
        # Display this text in the middle of the window
        draw_text_middle("Press any key to begin!", 60, (255, 255, 255), window)
        # Update the screen
        pygame.display.update()
        for event in pygame.event.get():
            # If the user presses any key, start playing the game!
            if event.type == pygame.KEYDOWN:
                play()
            # If user clicks on the 'cross' to quit, make run = False
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()


# DRIVER CODE
window = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Tetris")

game()