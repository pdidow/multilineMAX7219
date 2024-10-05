import time
import random
import threading
# Import library
import multilineMAX7219 as LEDMatrix
from multilineMAX7219 import *
# Import fonts
from multilineMAX7219_fonts import CP437_FONT, SINCLAIRS_FONT, LCD_FONT, TINY_FONT

# Initialise the library and the MAX7219/8x8LED arrays
LEDMatrix.init()

# ... (Your existing code for scrolling text and other setup)

# Set up LED matrix using multilineMAX7219
device = LEDMatrix(0, 8)  # Adjust parameters as needed

# Function to scroll text across the LED matrix
def scroll_text(device, text_to_scroll, font, speed=0.1):
    width = device.width
    height = device.height
    position = width

    while position >= -len(text_to_scroll) * 8:
        device.clear()
        with canvas(device) as draw:
            text(draw, (position, 2), text_to_scroll, fill="white", font=font)

        time.sleep(speed)
        position -= 1

# ... (Your existing code)

# Function to update the LED matrix display
def update_led_matrix(device, player_flash, monster_flash):
    with canvas(device) as draw:
        row_of_rooms = player_y // ROOM_HEIGHT
        for y in range(ROOM_HEIGHT):
            for x in range(WORLD_WIDTH):
                world_x = camera_x + x
                world_y = camera_y + (row_of_rooms * ROOM_HEIGHT) + y
                if world_x == player_x and world_y == player_y and player_flash:
                    draw.point((x, y), fill="white")  # Display player as white
                elif world_x == monster_x and world_y == monster_y and monster_flash:
                    draw.point((x, y), fill="red")    # Display monster as red
                elif 0 <= world_x < WORLD_WIDTH and 0 <= world_y < WORLD_HEIGHT:
                    if game_world[world_y][world_x] != '.':
                        draw.point((x, y), fill="green")  # Display other elements as green

# Main game loop
try:
    # Flag to control player flashing
    player_flash = True

    def player_flash_thread():
        global player_flash
        while True:
            time.sleep(0.5)  # Flash every 0.5 seconds
            player_flash = not player_flash

    # Start player flashing thread
    threading.Thread(target=player_flash_thread, daemon=True).start()

    # Flag to control monster flashing
    monster_flash = True

    def monster_flash_thread():
        global monster_flash
        while True:
            time.sleep(1)  # Flash every 1 second
            monster_flash = not monster_flash

    # Start monster flashing thread
    threading.Thread(target=monster_flash_thread, daemon=True).start()

    while True:
        # Clear the LED matrix
        device.clear()

        # Update and display the LED matrix
        update_led_matrix(device, player_flash, monster_flash)
        time.sleep(0.1)  # Adjust the sleep time as needed

        # Get player input
        move = input("Enter a move (W/A/S/D): ").upper()

        # ... (Your existing code for player movement and game logic)

except KeyboardInterrupt:
    # Cleanup when the program is interrupted
    device.cleanup()
