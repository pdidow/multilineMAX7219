#!/usr/bin/env python3

from Point import Point
import multilineMAX7219 as LEDMatrix
from multilineMAX7219 import GFX_ON, GFX_OFF, GFX_INVERT
from random import randrange
import threading
import sys
import time
from pydub import AudioSegment
from pydub.playback import play
USE_JOYPAD = False


#Modify this according to the physical orientation of your matrix's
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
#LOAD SOUNDS
eatMushroomSound = AudioSegment.from_wav("crunch1.wav")
deathSound = AudioSegment.from_wav("vgdeathsound.wav")


def display():
    LEDMatrix.gfx_set_all(GFX_OFF)

    # Draw the border
    for x in range(WIDTH + 1):
        LEDMatrix.gfx_set_px(x, 0, GFX_ON)  # Top border
        LEDMatrix.gfx_set_px(x, HEIGHT, GFX_ON)  # Bottom border

    for y in range(HEIGHT + 1):
        LEDMatrix.gfx_set_px(0, y, GFX_ON)  # Left border
        LEDMatrix.gfx_set_px(WIDTH, y, GFX_ON)  # Right border

    # Draw the walls
    for p in walls:
        LEDMatrix.gfx_set_px(int(p.x), int(p.y), GFX_ON)

    # Draw the snake and target
    for p in tail:
        LEDMatrix.gfx_set_px(int(p.x), int(p.y), GFX_ON)
    LEDMatrix.gfx_set_px(int(target.x), int(target.y), GFX_ON)

    LEDMatrix.gfx_render()
    global wasDisplayed
    wasDisplayed = True


def setTarget():
    global target
    target = Point(randrange(WIDTH + 1), randrange(HEIGHT + 1))
    while target in tail or target in walls:
        target = Point(randrange(WIDTH + 1), randrange(HEIGHT + 1))


def createWalls():
    global walls
    walls = []
    for _ in range(10):
        # Generate random wall with at least 3 dots together
        wall_size = randrange(3, 7)  # Adjust the size as needed
        start_point = Point(randrange(1, WIDTH - wall_size), randrange(1, HEIGHT - wall_size))
        walls.extend([start_point + Point(i, j) for i in range(wall_size) for j in range(wall_size)])


def move():
    global running, speed
    if running:
        newPosition = tail[0] + direction
        if (
            newPosition.x > WIDTH
            or newPosition.x < 0
            or newPosition.y > HEIGHT
            or newPosition.y < 0
            or newPosition in walls
        ):
            # Snake collided with the border or a wall, end the game
            running = False
            play(deathSound)
            for i in range(6):
                LEDMatrix.gfx_set_all(GFX_INVERT)
                LEDMatrix.gfx_render()
                time.sleep(0.3)
            if USE_JOYPAD:
                print("Game Over. Score:", len(tail) - 1)
            else:
                print("Game Over. Press any Key to exit. Score:", len(tail) - 1)
            LEDMatrix.clear_all()
            sys.exit("\n")

        if newPosition == target:
            play(eatMushroomSound)
            tail.insert(0, newPosition)
            setTarget()
            speed = max(0.07, min(0.3, 2 / float(len(tail))))
        elif newPosition not in tail:
            tail.insert(0, newPosition)
            tail.pop()
        else:
            # Game Over
            running = False
            for i in range(6):
                LEDMatrix.gfx_set_all(GFX_INVERT)
                LEDMatrix.gfx_render()
                time.sleep(0.3)
            if USE_JOYPAD:
                print("Game Over. Score:", len(tail) - 1)
            else:
                print("Game Over. Press any Key to exit. Score:", len(tail) - 1)
            LEDMatrix.clear_all()
            sys.exit("\n")

        # threading for calling it every period
        threading.Timer(speed, move).start()
    else:
        LEDMatrix.clear_all()
    display()


def changeDirection(newDirection=direction):
    global direction, wasDisplayed
    if wasDisplayed:
        if newDirection != direction and (
            newDirection.x != -direction.x or newDirection.y != -direction.y
        ):
            direction = newDirection
            wasDisplayed = False


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
