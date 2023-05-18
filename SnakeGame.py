import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import animation
from matplotlib.widgets import Button

# The snake is represented as a list of (x, y) coordinates
# The first element of the list is the head of the snake
snake = [(3, 3), (3, 2), (3, 1)]
direction = 'up'

# The food is represented as an (x, y) coordinate
food = (6, 6)

score = 0

# Initialize the plot
fig, ax = plt.subplots()

def draw():
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks(np.arange(0, 11, 1))
    ax.set_yticks(np.arange(0, 11, 1))
    ax.grid()

    # Draw the snake
    for segment in snake:
        ax.text(*segment, 's', va='center', ha='center')

    # Draw the food
    ax.text(*food, 'f', va='center', ha='center')

    ax.set_title(f'Score: {score}')

def step():
    global snake, direction, food, score
    # Calculate the new head position based on the current direction
    if direction == 'up':
        new_head = (snake[0][0], snake[0][1]+1)
    elif direction == 'down':
        new_head = (snake[0][0], snake[0][1]-1)
    elif direction == 'left':
        new_head = (snake[0][0]-1, snake[0][1])
    elif direction == 'right':
        new_head = (snake[0][0]+1, snake[0][1])
    # Check if the game is over
    if new_head in snake or new_head[0] < 0 or new_head[0] >= 10 or new_head[1] < 0 or new_head[1] >= 10:
        return False
    # Check if the snake has eaten the food
    if new_head == food:
        score += 1
        food = (random.randint(0, 9), random.randint(0, 9))
    else:
        # If the snake didn't eat food, then it moves forward and its tail is removed
        snake.pop()
    # The new head is added to the snake
    snake.insert(0, new_head)
    return True

def animate(i):
    if not step():
        return
    draw()

def on_key(event):
    global direction
    if event.key == 'up':
        direction = 'up'
    elif event.key == 'down':
        direction = 'down'
    elif event.key == 'left':
        direction = 'left'
    elif event.key == 'right':
        direction = 'right'

fig.canvas.mpl_connect('key_press_event', on_key)
ani = animation.FuncAnimation(fig, animate, interval=200)

plt.show()
