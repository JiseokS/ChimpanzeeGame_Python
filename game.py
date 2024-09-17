import pygame
import pygame_gui
from random import *
import sys
import psycopg2

def get_user_name(screen, manager):

    global name
    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
                name = event.text
                return name
                
            manager.process_events(event)
        
        manager.update(UI_REFRESH_RATE)

        screen.fill(BLACK)

        manager.draw_ui(screen)

        pygame.display.update()

def setup(level):
    
    number_count = (level // 3) + 5
    
    shuffle_grid(number_count)

# Shuffle number
def shuffle_grid(number_count):
    rows = 5
    columns = 9

    cell_size = 130    # Each grid cell size (width, height)
    button_size = 110   # Button size
    screen_left_margin = 55
    screen_top_margin = 20 

    # [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    grid = [[0 for col in range(columns)] for row in range(rows)] # 5 x 9

    number = 1  # start number 1 to number_count
    while number <= number_count:
        row_idx = randrange(0, rows)    # Random select between 0, 1, 2, 3, 4
        col_idx = randrange(0, columns) # Random select between 0, 1, 2, 3, 4, 5, 6, 7, 8

        if grid[row_idx][col_idx] == 0:
            grid[row_idx][col_idx] = number 
            number += 1

            # Get x,y location based on current grid cell location
            center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)

            # Number Button generate
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button)
    # print(grid)
    
    print(grid)


def display_start_screen(screen, curr_level):
    start_button = pygame.Rect(0, 0, 120, 120)
    start_button.center = (120, screen.get_height() - 120)
    
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)
    
    msg = game_font.render(f"{curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=start_button.center)
    screen.blit(msg, msg_rect)
    pygame.display.update()

# Game screen display 
def display_game_screen():
    global hidden

    for idx, rect in enumerate(number_buttons, start=1):
        if hidden: 
            # Draw rectangle button
            pygame.draw.rect(screen, WHITE, rect)
        else:
           # Number text
            cell_text = game_font.render(str(idx), True, WHITE)
            text_rect = cell_text.get_rect(center=rect.center)
            screen.blit(cell_text, text_rect)



def check_buttons(pos):
    global start

    if start:
        check_number_buttons(pos)
    elif start_button.collidepoint(pos):
        start = True

def check_number_buttons(pos):
    global start, hidden, curr_level

    for button in number_buttons:
        if button.collidepoint(pos):
            if button == number_buttons[0]: 
                print("Correct")  
                del number_buttons[0]  # Delete first number 
                if not hidden:
                    hidden = True      # Hidden number
            else: # Wrong number click
                game_over()
            break

    # If click all correct numbers, go to next level       
    if len(number_buttons) == 0:
        start = False
        hidden = False
        curr_level += 1
        setup(curr_level) 


def game_over():
    global running, name, curr_level
    running = False
    
    conn = psycopg2.connect()
    cur = conn.cursor()

    cur.execute("INSERT INTO scores (player_name, score) VALUES (%s, %s)", (name, curr_level))
    conn.commit()

    cur.close()
    conn.close()

    msg = game_font.render(f"{name}'s score - {curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=(screen_width/2, screen_height/2))

    screen.fill(BLACK)
    screen.blit(msg, msg_rect)
# reset
pygame.init()
name = ""
clock = pygame.time.Clock()
screen_width = 1280
screen_height = 720 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Memory Game")
game_font = pygame.font.Font(None, 120) 


start_button = pygame.Rect(0, 0, 120, 120)
start_button.center = (120, screen_height - 120)


BLACK = (0, 0, 0) # RGB 
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

number_buttons = [] # The buttons that player have to click
curr_level = 1 # Current level set 1
display_time = None 
start_ticks = None 

# Start Game
start = False
# Number hidden (user click 1)
hidden = False


setup(curr_level) # Setup game before game start

SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Text Input in PyGame | BaralTech")

manager = pygame_gui.UIManager((1600, 900))

text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (600, 50)), manager=manager,
                                               object_id='#main_text_entry')

UI_REFRESH_RATE = clock.tick(60)/1000

# Game Loop
running = True  # Check the game running
name_entered = False  # Flag to track whether the user has entered their name
show_name_input = True  # Flag to control rendering of the name input field
while running:
    click_pos = None
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # Close Window
            running = False           # Game is not runnings
        elif event.type == pygame.MOUSEBUTTONUP: # When user click mouse
            click_pos = pygame.mouse.get_pos()
            print(click_pos)
        
        # Process events for the text input
        manager.process_events(event)

    screen.fill(BLACK)

    if not start:
        if not name_entered and show_name_input:
            user_name = get_user_name(screen, manager)  
            if user_name:
                name_entered = True
                show_name_input = False
        else:
            display_start_screen(screen, curr_level)  # Show the start screen after getting user name
    else: 
        display_game_screen() 

    if click_pos:
        check_buttons(click_pos)
    # Update the GUI manager
    manager.update(UI_REFRESH_RATE)
    
    # Draw UI elements based on game state
    if show_name_input:
        manager.draw_ui(screen)
    # Display Update
    pygame.display.update()



pygame.time.delay(5000)

# Game End
# Close database connection
cur.close()
conn.close()
pygame.quit