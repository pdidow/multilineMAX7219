from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
import time
import random
import threading
from luma.core.legacy import text, show_message
from luma.core.legacy.font import  TINY_FONT

# Function to scroll text across the LED matrix
def scroll_text(device, text_to_scroll, font, speed=0.1):
    width = device.width
    height = device.height
    position = width

    while position >= -len(text_to_scroll) * 8:
        with canvas(device) as draw:
            text(draw, (position, 2), text_to_scroll, fill="white", font=font)

        time.sleep(speed)
        position -= 1

# Set up LED matrix
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=8, block_orientation=-90, rotate=2, width=32, height=16)  # Adjust parameters as needed

# Scroll "LED Venture" in TINY_FONT
scroll_text(device, "Welcome Adventurer to LED Venture!!!", TINY_FONT, speed=.02)

# Clear the LED matrix
device.clear()

# Define the dimensions of the game world
WORLD_WIDTH = 32  # Four 8x8 rooms in a row
WORLD_HEIGHT = 32  # Four rows of 8x8 rooms

# Define the player and monster positions within the world
player_x = WORLD_WIDTH // 2  # Set default player_x to the center of the game world
player_y = WORLD_HEIGHT // 2  # Set default player_y to the center of the game world
monster_x = random.randint(0, WORLD_WIDTH - 1)
monster_y = random.randint(0, WORLD_HEIGHT - 1)

# Create a function to initialize the game world from a map file
def initialize_world_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    game_world = [list(line.strip()) for line in lines]

    # Find the initial player position (P) and monster position (M) in the map
    for y in range(len(game_world)):
        for x in range(len(game_world[y])):
            if game_world[y][x] == 'P':
                player_x = x
                player_y = y
            elif game_world[y][x] == 'M':
                monster_x = x
                monster_y = y

    return game_world

# Load the map from the 'venture.map' file
game_world = initialize_world_from_file('venture.map')

# Define the size of the 8x8 room
ROOM_WIDTH = 8
ROOM_HEIGHT = 8

# Define the camera position (initially centered)
camera_x = max(0, player_x - ROOM_WIDTH * 2)
camera_y = max(0, player_y - ROOM_HEIGHT * 2)

# Create a function to find a random open space for the monster
def find_random_open_space():
    while True:
        x = random.randint(0, WORLD_WIDTH - 1)
        y = random.randint(0, WORLD_HEIGHT - 1)
        if game_world[y][x] == '.':
            return x, y

# Get a random open space for the monster
monster_x, monster_y = find_random_open_space()

# Function to move the monster towards the player
def move_monster_towards_player():
    global monster_x, monster_y
    if monster_x < player_x and game_world[monster_y][monster_x + 1] != '#':
        monster_x += 1
    elif monster_x > player_x and game_world[monster_y][monster_x - 1] != '#':
        monster_x -= 1
    if monster_y < player_y and game_world[monster_y + 1][monster_x] != '#':
        monster_y += 1
    elif monster_y > player_y and game_world[monster_y - 1][monster_x] != '#':
        monster_y -= 1

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

        # Update player position
        new_player_x = player_x
        new_player_y = player_y
        if move == 'W' and player_y > 0 and game_world[player_y - 1][player_x] != '#':
            new_player_y -= 1
        elif move == 'A' and player_x > 0 and game_world[player_y][player_x - 1] != '#':
            new_player_x -= 1
        elif move == 'S' and player_y < WORLD_HEIGHT - 1 and game_world[player_y + 1][player_x] != '#':
            new_player_y += 1
        elif move == 'D' and player_x < WORLD_WIDTH - 1 and game_world[player_y][player_x + 1] != '#':
            new_player_x += 1

        # Update camera position when the player crosses room boundaries
        if new_player_x < camera_x:
            camera_x = max(0, new_player_x - ROOM_WIDTH * 2)
        elif new_player_x >= camera_x + ROOM_WIDTH * 4:
            camera_x = min(WORLD_WIDTH - ROOM_WIDTH * 4, new_player_x - ROOM_WIDTH * 2)
        if new_player_y < camera_y:
            camera_y = max(0, new_player_y - ROOM_HEIGHT * 2)
        elif new_player_y >= camera_y + ROOM_HEIGHT * 4:
            camera_y = min(WORLD_HEIGHT - ROOM_HEIGHT * 4, new_player_y - ROOM_HEIGHT * 2)

        # Update player position
        player_x = new_player_x
        player_y = new_player_y

        # Move the monster towards the player
        move_monster_towards_player()

        # Check for collisions with the monster
        if player_x == monster_x and player_y == monster_y:
           print("You encountered a monster! Game over.")
           # Scroll "LED Venture" in TINY_FONT
           scroll_text(device, "*** GAME OVER ***", tiny, speed=0.1)

        break

except KeyboardInterrupt:
    # Cleanup when the program is interrupted
    device.cleanup()
