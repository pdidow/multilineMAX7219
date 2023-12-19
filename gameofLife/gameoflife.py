#!/usr/bin/env python3

from Point import Point
import multilineMAX7219 as LEDMatrix
from multilineMAX7219 import GFX_ON, GFX_OFF, GFX_INVERT
import threading
import time
import copy
from random import randrange
WIDTH = 32
HEIGHT = 24

# Initialize LEDMatrix
LEDMatrix.init()

# Initialize the Game of Life grid
grid = [[0] * HEIGHT for _ in range(WIDTH)]

# Define the directions for neighboring cells
NEIGHBOR_DIRECTIONS = [
    Point(-1, -1), Point(0, -1), Point(1, -1),
    Point(-1, 0),                 Point(1, 0),
    Point(-1, 1), Point(0, 1), Point(1, 1)
]

# Function to initialize the grid randomly
def initialize_grid():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            grid[x][y] = randrange(2)

# Function to display the Game of Life grid on the LED matrix
def display_grid():
    LEDMatrix.gfx_set_all(GFX_OFF)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if grid[x][y] == 1:
                LEDMatrix.gfx_set_px(x, y, GFX_ON)
    LEDMatrix.gfx_render()

# Function to determine the next state of a cell based on the rules of the Game of Life
def get_next_state(x, y):
    live_neighbors = sum(grid[int((x + dx) % WIDTH)][int((y + dy) % HEIGHT)] for dx, dy in NEIGHBOR_DIRECTIONS)
    if grid[x][y] == 1:
        return 1 if live_neighbors in [2, 3] else 0
    else:
        return 1 if live_neighbors == 3 else 0

# Function to update the Game of Life grid to the next generation
def update_grid():
    new_grid = copy.deepcopy(grid)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            new_grid[x][y] = get_next_state(x, y)
    return new_grid

# Main loop
if __name__ == "__main__":
    initialize_grid()

    while True:
        display_grid()
        time.sleep(1)  # Adjust the delay based on your preference
        grid = update_grid()
