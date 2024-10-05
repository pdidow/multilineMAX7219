from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
import time
from luma.core.legacy import text
from luma.core.legacy.font import TINY_FONT

# Function to display static text on the LED matrix
def display_text(device, text_to_display, font):
    with canvas(device) as draw:
        # Display the text in a fixed position, adjust (x, y) if needed
        text(draw, (0, 2), text_to_display, fill="white", font=font)

# Set up the LED matrix
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=12, block_orientation=-90, rotate=2, width=32, height=24)  # Adjust parameters as needed

# Display the text once
display_text(device, "Welcome\nAdventurer!", TINY_FONT)

# Hold the text on the display for 5 seconds (adjust as needed)
time.sleep(5)

# Clear the LED matrix after the delay
device.clear()

# Program ends here, and display is cleared
