import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import animation
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button
import pickle

# The snake is represented as a list of (x, y) coordinates
snake = [(15, 15), (15, 14), (15, 13)]
direction = 'up'

# The food is represented as an (x, y) coordinate
food = (20, 20)

score = 0
level = 1

# Load high score
try:
    with open('high_score.pkl', 'rb') as f:
        high_score = pickle.load(f)
except FileNotFoundError:
    high_score = 0

# game state
game_state = 'run'  # 'run', 'gameover'

# Initialize the plot
fig = plt.figure(figsize=(8, 9))
gs = fig.add_gridspec(11, 10)
ax = fig.add_subplot(gs[:-1, :])  # The main playing area
ax_button = fig.add_subplot(gs[-1, 4:6])  # The area for start button

# Add a start button
button_start = Button(ax_button, 'Start', color='lightgreen', hovercolor='green')

# Function to save high score
def save_high_score():
    with open('high_score.pkl', 'wb') as f:
        pickle.dump(high_score, f)

def draw():
    ax.clear()
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 30)
    ax.axis('off')

    # Set background color
    if game_state == 'run':
        fig.patch.set_facecolor('black')
    else:
        fig.patch.set_facecolor('darkred')

    ax.set_facecolor('black')

    # Add white borders
    for side in ['top', 'bottom', 'right', 'left']:
        ax.spines[side].set_visible(True)
        ax.spines[side].set_color('white')
        ax.spines[side].set_linewidth(10)

    # Draw white border
    rectangle = Rectangle((0, 0), 30, 30, fill=False, edgecolor='white', linewidth=3)
    ax.add_patch(rectangle)


    # Draw the snake
    for segment in snake:
        rectangle = Rectangle((segment[0]+0.1, segment[1]+0.1), 0.8, 0.8, edgecolor='green', facecolor='green')
        ax.add_patch(rectangle)

    # Draw the food
    star = plt.Line2D((food[0]+0.5, ), (food[1]+0.5, ), color='red', marker='*', linestyle='')
    ax.add_line(star)

    ax.set_title(f'Level: {level}  Score: {score}  High Score: {high_score}', color='white')

    if game_state == 'gameover':
        ax.text(15, 15, 'Game Over', va='center', ha='center', color='white', size=30)

def step():
    global snake, direction, food, score, high_score, game_state, level
    if game_state == 'run':
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
        if new_head in snake or new_head[0] < 0 or new_head[0] >= 30 or new_head[1] < 0 or new_head[1] >= 30:
            # Update high score
            if score > high_score:
                high_score = score
                save_high_score()
            game_state = 'gameover'
            return
        # Check if the snake has eaten the food
        if (abs(new_head[0]-food[0])<1) and (abs(new_head[1]-food[1])<1):
            score += 1
            food = (random.randint(0, 29), random.randint(0, 29))
            if score % 5 == 0:  # Increase level every 5 points
                level += 1
        else:
            # If the snake didn't eat food, then it moves forward and its tail is removed
            snake.pop()
        # The new head is added to the snake
        snake.insert(0, new_head)



def animate(i):
    global level
    # Move the snake once every n frames, where n = max(1, 5 - level)
    if i % max(1, 5 - level) == 0:
        step()
    draw()

def on_key(event):
    global direction
    if game_state == 'run':
        if event.key == 'up' and direction != 'down':
            direction = 'up'
        elif event.key == 'down' and direction != 'up':
            direction = 'down'
        elif event.key == 'left' and direction != 'right':
            direction = 'left'
        elif event.key == 'right' and direction != 'left':
            direction = 'right'

def start_game(event):
    global snake, direction, food, score, game_state, level
    game_state = 'run'
    snake = [(15, 15), (15, 14), (15, 13)]
    direction = 'up'
    food = (20, 20)
    score = 0
    level = 1

def on_close(event):
    if score > high_score:
        save_high_score()

fig.canvas.mpl_connect('close_event', on_close)
button_start.on_clicked(start_game)
fig.canvas.mpl_connect('key_press_event', on_key)
ani = animation.FuncAnimation(fig, animate, interval=20, save_count=500)

plt.show()
