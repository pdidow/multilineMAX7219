#!/usr/bin/env python3

from Point import Point
import multilineMAX7219 as LEDMatrix
from multilineMAX7219 import GFX_ON, GFX_OFF, GFX_INVERT
import threading
import sys
import time
from pydub import AudioSegment
from pydub.playback import play
from random import randrange
USE_JOYPAD = False

DIR_U = Point(1, 0)
DIR_D = Point(-1, 0)
DIR_R = Point(0, -1)
DIR_L = Point(0, 1)

WIDTH = 8 * LEDMatrix.MATRIX_WIDTH - 1
HEIGHT = 8 * LEDMatrix.MATRIX_HEIGHT - 1

tail = [Point(WIDTH // 2, HEIGHT // 2)]
start = randrange(2)
direction = Point(start, 1 - start)

target = Point()
running = True
speed = 0.3
wasDisplayed = True

walls = []

LEDMatrix.init()
eatMushroomSound = AudioSegment.from_wav("crunch1.wav")
deathSound = AudioSegment.from_wav("vgdeathsound.wav")

def load_walls_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return [[int(char) for char in line.strip()] for line in lines]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

def display_walls():
    for x, row in enumerate(walls):
        for y, has_wall in enumerate(row):
            if has_wall:
                LEDMatrix.gfx_set_px(x, y, GFX_ON)

def is_valid_target_position(pos):
    return pos not in tail and not walls[pos.x][pos.y]

def setTarget():
    global target
    target = Point(randrange(WIDTH + 1), randrange(HEIGHT + 1))
    while not is_valid_target_position(target):
        target = Point(randrange(WIDTH + 1), randrange(HEIGHT + 1))

def createWalls():
    global walls
    walls = load_walls_from_file("walls1.txt")

def move():
    # ... (rest of the code remains unchanged)

    if __name__ == "__main__":
        setTarget()
        createWalls()
        move()

    if USE_JOYPAD:
        try:
            print("To end the game press <CTRL> + C")
            while running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nGoodbye")
            LEDMatrix.clear_all()
            time.sleep(0.1)
            running = False
    else:
        from _Getch import _Getch

        getch = _Getch()
        print("To end the game press <q>")
        while running:
            key = ord(getch())
            if key == 27:  # ESC
                key = ord(getch())
                if key == 91:
                    key = ord(getch())
                    if key == 65:  # Up arrow
                        changeDirection(DIR_U)
                    if key == 66:  # Down arrow
                        changeDirection(DIR_D)
                    elif key == 67:  # right arrow
                        changeDirection(DIR_R)
                    elif key == 68:  # left arrow
                        changeDirection(DIR_L)
            elif key == 113:
                print("Goodbye")
                running = False
                break

