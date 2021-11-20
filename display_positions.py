#!/usr/bin/env python
# ---------------------------------------------------------
# Filename: display_positions.py
# ---------------------------------------------------------
# This script will display a number on each MAX7219. 
# First one will get 0, second one 1 and so on.
# Use this script to check if your matrices match the numbering
# used in the multilineMAX7219.py library.
# If the numbers are upside down, set ROTATE_BLOCKS_BY_180_DEGREES
# to True. 
#
# The variables MATRIX_WIDTH and MATRIX_HEIGHT, defined in the 
#	multilineMAX7219.py library script, should always be set to be 
#	consistent with the actual hardware setup in use.
# ---------------------------------------------------------

import time
import math
from random import randrange

# Import library
import multilineMAX7219 as LEDMatrix
from multilineMAX7219 import *
# Import fonts
from multilineMAX7219_fonts import CP437_FONT, SINCLAIRS_FONT, LCD_FONT, TINY_FONT

# Initialise the library and the MAX7219/8x8LED arrays
LEDMatrix.init()

print ("Do not forget to update MATRIX_WIDTH and MATRIX_HEIGHT in multilineMAX7219.py prior this test")

try:
	LEDMatrix.clear_all()

	LEDMatrix.brightness(0)
	# Display all characters from the font individually
	for char in range(NUM_MATRICES):
		LEDMatrix.send_matrix_letter(char, ord("%0.1X" % (char%16)))
		time.sleep(0.22)
	time.sleep(0.5)
except:
	print ("display error. Check M x N configuration library")
