import sys
from multilineMAX7219 import GFX_ON, GFX_OFF, GFX_INVERT

# Import library
import multilineMAX7219 as LEDMatrix

# Initialise the library and the MAX7219/8x8LED arrays
LEDMatrix.init()

def draw_pixel(x, y):
    # Turn on the pixel
    LEDMatrix.gfx_set_px(x, y, GFX_ON)

    # Render the changes
    LEDMatrix.gfx_render()

if __name__ == "__main__":
    # Check if x and y are provided as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <x> <y>")
        sys.exit(1)

    try:
        # Parse x and y from command-line arguments
        x = int(sys.argv[1])
        y = int(sys.argv[2])

        # Check if coordinates are within bounds
        if not (0 <= x < LEDMatrix.MATRIX_WIDTH and 0 <= y < LEDMatrix.MATRIX_HEIGHT):
            print("Invalid coordinates. x and y must be within bounds.")
            sys.exit(1)

        draw_pixel(x, y)

    except ValueError:
        print("Invalid coordinates. Please provide integers for x and y.")
        sys.exit(1)
