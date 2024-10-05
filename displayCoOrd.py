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



# Assuming LEDMatrix is already initialized
LEDMatrix.init()

# Coordinates of the pixel
x = 2
y = 0

# Turn on the pixel
LEDMatrix.gfx_set_px(x, y, GFX_ON)

# Render the changes
LEDMatrix.gfx_render()
