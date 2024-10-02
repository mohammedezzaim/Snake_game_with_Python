import random
import curses
import sys
import time

# Function to clean up and close the game
# Function to clean up and close the game
def end_game():
    curses.endwin()
    sys.exit()

# initialize the curses library to create our screen
screen = curses.initscr()

curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Serpent en vert tete
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Nourriture en jaune
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # Red boy and end de serpont

# hide the mouse cursor
curses.curs_set(0)

# get max screen height and width
screen_height, screen_width = screen.getmaxyx()

# create a new window
window = curses.newwin(screen_height, screen_width, 0, 0)

# allow window to receive input from the keyboard
window.keypad(True)

# set the delay for updating the screen
window.timeout(125)

# set the x, y coordinates of the initial position of snake's head
snk_x = screen_width // 4
snk_y = screen_height // 2

# define the initial position of the snake body
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1],
    [snk_y, snk_x - 2]
]

# create the food in the middle of the window
food = [screen_height // 2, screen_width // 2]

# add the food as a point character ('.') in yellow
window.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(2))

# set initial movement direction to right
key = curses.KEY_RIGHT

# create game loop that loops forever until player loses or quits the game
while True:
    next_key = window.getch()
    key = key if next_key == -1 else next_key

    # check if snake hits the wall or itself
    if (snake[0][0] in [0, screen_height] or 
        snake[0][1] in [0, screen_width] or 
        snake[0] in snake[1:]):
        end_game()

    # create new head based on current direction
    new_head = [snake[0][0], snake[0][1]]

    if key == curses.KEY_DOWN:
        new_head[0] += 1
    elif key == curses.KEY_UP:
        new_head[0] -= 1
    elif key == curses.KEY_RIGHT:
        new_head[1] += 1
    elif key == curses.KEY_LEFT:
        new_head[1] -= 1

    # insert new head at the start of snake
    snake.insert(0, new_head)

    # check if snake eats food
    if snake[0] == food:
        food = None
        while food is None:
            new_food = [
                random.randint(1, screen_height - 2),
                random.randint(1, screen_width - 2)
            ]
            food = new_food if new_food not in snake else None

        # add the new food as a point character ('.') in yellow
        window.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(2))
    else:
        # move snake: remove tail
        tail = snake.pop()
        window.addch(tail[0], tail[1], ' ')

    for segment in snake[1:]:
        window.addch(segment[0], segment[1], curses.ACS_CKBOARD | curses.color_pair(3))  # Corps du serpent

    # draw the snake's new head
    window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD | curses.color_pair(1))
