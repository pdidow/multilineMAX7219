#!/usr/bin/env python
# ---------------------------------------------------------
# Filename: multilineMAX7219_demo.py
# ---------------------------------------------------------
# Demonstration of the features in the multilineMAX7219 library
#
# v1.0
# F.Stern 2014
# ---------------------------------------------------------
# improved and extended version of JonA1961's MAX7219array
# ( https://github.com/JonA1961/MAX7219array )
# ---------------------------------------------------------
# See multilineMAX7219.py library file for more details
# ---------------------------------------------------------
# This demo script is intended to run on an array of 9 (3x3)
#   MAX7219 boards, connected as described in the library
#   script. 
# The variables MATRIX_WIDTH and MATRIX_HEIGHT, defined in the 
#   multilineMAX7219.py library script, should always be set to be 
#   consistent with the actual hardware setup in use.  If it is 
#   not set correctly, then the functions will not work as
#   intended
# ---------------------------------------------------------

import time
from random import randrange

# Import library
import multilineMAX7219 as LEDMatrix
# Import fonts
from multilineMAX7219_fonts import CP437_FONT, SINCLAIRS_FONT, LCD_FONT, TINY_FONT

# The following imported variables make it easier to feed parameters to the library functions
from multilineMAX7219 import DIR_L, DIR_R, DIR_U, DIR_D
from multilineMAX7219 import DIR_LU, DIR_RU, DIR_LD, DIR_RD
from multilineMAX7219 import DISSOLVE, GFX_ON, GFX_OFF, GFX_INVERT

# Initialise the library and the MAX7219/8x8LED arrays
LEDMatrix.init()

try:
    # Define Pacman image as a pixel map
    pacman = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 0]
    ]

    # Define Pacman2 image as a pixel map
    pacman2 = [
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 0, 0]
    ]

    # Define Pacman3 image as a pixel map
    pacman3 = [
    [0, 0, 0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 0, 0]
    ]

    LEDMatrix.gfx_set_all(GFX_OFF)
    LEDMatrix.gfx_sprite_array(pacman, 7, 8)
    LEDMatrix.gfx_render()
    time.sleep(1)

    LEDMatrix.gfx_set_all(GFX_OFF)
    LEDMatrix.gfx_sprite_array(pacman2,7,8)
    LEDMatrix.gfx_render()
    time.sleep(1)

    LEDMatrix.gfx_set_all(GFX_OFF)
    LEDMatrix.gfx_sprite_array(pacman3,7,8)
    LEDMatrix.gfx_render()
    time.sleep(1)


    for repeat in range(2):
        for scroll in (DIR_L, DIR_LU, DIR_U, DIR_RU, DIR_R, DIR_RD, DIR_D, DIR_LD):
            moves = 2 * repeat + 1
            if scroll in [DIR_R, DIR_RD, DIR_D, DIR_LD]:
                moves += 1
            for loop in range(moves):
                LEDMatrix.gfx_scroll(scroll)
                LEDMatrix.gfx_render()
                time.sleep(0.1)
    time.sleep(1)

except KeyboardInterrupt:
    # reset array
    LEDMatrix.scroll_message_horiz(["", "Goodbye!", ""], 1, 8)
    LEDMatrix.clear_all()
