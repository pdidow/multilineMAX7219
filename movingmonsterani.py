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
    # Define hallmonster image as a pixel map
    hallmonster_frame1 = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 1, 0, 1, 0],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    ]


    # Define hallmonster2 image as a pixel map
    hallmonster_frame2 = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 1, 0, 1, 0],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    ]


# Define hallmonster3 image as a pixel map
    hallmonster_frame3 = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 1, 0, 1, 0],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
    ]


    # Initialize hallmonster position
    hallmonster_x = 0
    hallmonster_y = 0
    #Flip the frames vertically
    hallmonster_frame1= list(reversed(hallmonster_frame1))
    hallmonster_frame2= list(reversed(hallmonster_frame2))
    hallmonster_frame3= list(reversed(hallmonster_frame3))
    # Display Pacman animation forever
    while True:
        LEDMatrix.gfx_set_all(GFX_OFF)
        LEDMatrix.gfx_sprite_array(hallmonster_frame1, hallmonster_x,hallmonster_y)
        LEDMatrix.gfx_render()
        time.sleep(0.1)

        LEDMatrix.gfx_set_all(GFX_OFF)
        LEDMatrix.gfx_sprite_array(hallmonster_frame2, hallmonster_x, hallmonster_y)
        LEDMatrix.gfx_render()
        time.sleep(0.1)

        LEDMatrix.gfx_set_all(GFX_OFF)
        LEDMatrix.gfx_sprite_array(hallmonster_frame3, hallmonster_x, hallmonster_y)
        LEDMatrix.gfx_render()
        time.sleep(0.1)

        # Update hallmonster position
        
        hallmonster_y+=1
        if hallmonster_y >24:
           hallmonster_y = 0
        
            
        if hallmonster_x<=32:
           hallmonster_x+=8
        else:
            hallmonster_x=0

except KeyboardInterrupt:
    # reset array
    LEDMatrix.scroll_message_horiz(["", "Goodbye!", ""], 1, 8)
    LEDMatrix.clear_all()
