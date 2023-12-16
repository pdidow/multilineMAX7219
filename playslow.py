#!/usr/bin/env python
import time
import os
import sys
import multilineMAX7219 as LEDMatrix
from multilineMAX7219_fonts import CP437_FONT, SINCLAIRS_FONT, LCD_FONT, TINY_FONT
from multilineMAX7219 import DIR_L, DIR_R, DIR_U, DIR_D
from multilineMAX7219 import DIR_LU, DIR_RU, DIR_LD, DIR_RD
from multilineMAX7219 import DISSOLVE, GFX_ON, GFX_OFF, GFX_INVERT

def read_sprite_files(folder_name):
    sprites = []
    for filename in os.listdir(folder_name):
        if filename.startswith("sprite_") and filename.endswith(".txt"):
            file_path = os.path.join(folder_name, filename)
            with open(file_path, "r") as file:
                try:
                    content_str = file.read().replace('[', '').replace(']', '').replace(',', ' ')
                    rows = content_str.split('\n')
                    content = [[int(num) for num in row.split()] for row in rows if row]
                    # Reverse each sprite vertically
                    reversed_sprite = list(reversed(content))
                    sprites.append(reversed_sprite)
                except ValueError as e:
                    print(f"Error reading file {filename}: {e}")
    return sprites

if len(sys.argv) != 2:
    print("Usage: python devilDance.py <folder_name>")
    sys.exit(1)

folder_name = sys.argv[1]

# Initialise the library and the MAX7219/8x8LED arrays
LEDMatrix.init()

# Define animation frames by reading sprite files
animation_frames = read_sprite_files(folder_name)
#flip horizontal
animation_frames = list(reversed(animation_frames))

try:
    # Display animation forever
    while True:
        for frame in animation_frames:
            LEDMatrix.gfx_set_all(GFX_OFF)
            LEDMatrix.gfx_sprite_array(frame, 1, 8)
            LEDMatrix.gfx_render()
            time.sleep(0.5)

except KeyboardInterrupt:
    # Reset array
    LEDMatrix.scroll_message_horiz(["", "Goodbye!", ""], 1, 8)
    LEDMatrix.clear_all()
