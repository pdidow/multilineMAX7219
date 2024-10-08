#!/usr/bin/env python
# ---------------------------------------------------------
# Filename: devilDance.py
# ---------------------------------------------------------
# Demonstration of the features in the multilineMAX7219 library
#
# v1.0
# F.Stern 2014
# ---------------------------------------------------------
# Improved and extended version of JonA1961's MAX7219array
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
import datetime
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

def display_rotated_char(char_matrix, graphics_mode):
    rotated_char = LEDMatrix.rotate_char_90_degrees(char_matrix)
    LEDMatrix.gfx_set_all(GFX_OFF)
    LEDMatrix.gfx_sprite_array(rotated_char, 0, 1, graphics_mode)
    LEDMatrix.gfx_render()
    time.sleep(0.5)

try:
    # Define Devil image1 as a pixel map
    devil1 = [
        [0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 0, 1, 1, 1, 1, 0, 1],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0]
    ]

    # Define Devil2 image2 as a pixel map
    devil2 = [
        [0, 0, 1, 0, 0, 1, 0, 0],
        [1, 0, 1, 1, 1, 1, 0, 0],
        [1, 0, 1, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 0, 1],
        [0, 0, 1, 1, 1, 1, 0, 1],
        [0, 0, 1, 1, 1, 1, 0, 1],
        [0, 0, 1, 0, 0, 1, 0, 0]
    ]
    # Flip the frames vertically
    devil1 = list(reversed(devil1))
    devil2 = list(reversed(devil2))

    # Display Pacman animation forever
    while True:
        display_rotated_char(devil1, GFX_OFF)
        display_rotated_char(devil2, GFX_OFF)

        # Get the current date and time
        current_time = datetime.datetime.now()

        # Format the current time as a string
        formatted_time = current_time.strftime("%I:%M %p")

        # Scroll the message horizontally
        speed = 6
        LEDMatrix.scroll_message_horiz(["", formatted_time, ""], 1, 8)
        #LEDMatrix.static_message("",formatted_time,"")
except KeyboardInterrupt:
    # reset array
    LEDMatrix.scroll_message_horiz(["", "Goodbye!", ""], 1, 8)
    LEDMatrix.clear_all()
