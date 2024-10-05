import multilineMAX7219 as LEDMatrix
# Import fonts
from multilineMAX7219_fonts import CP437_FONT, SINCLAIRS_FONT, LCD_FONT, TINY_FONT
from multilineMAX7219 import GFX_ON, GFX_OFF, GFX_INVERT
import time
import random
import threading
import pygame
import math
from _Getch import _Getch
from include.asteroid import Asteroid, AsteroidTypes
from point import Point



# Constants
WIDTH = 8 * LEDMatrix.MATRIX_WIDTH - 1
HEIGHT = 8 * LEDMatrix.MATRIX_HEIGHT - 1
SHIP_SIZE = 4
ASTEROID_SIZE = 4
INITIAL_ASTEROID_COUNT = 5
MAX_ASTEROID_COUNT = 10
GRID_WIDTH = 32
GRID_HEIGHT=24



# 4x4 Grid Representation of the Ship
SHIP_GRID = [
    [0, 1, 0,0],
    [0, 1, 1,1],
    [0, 1, 1,1],
    [0, 1, 0,0]
	
]

ASTEROID_TYPE_1 = [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
]

ASTEROID_TYPE_2 = [
    [0, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 0, 1],
    [0, 1, 1, 0]
]

ASTEROID_TYPE_3 = [
    [1, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 1]
]

ASTEROID_TYPES = [ASTEROID_TYPE_1, ASTEROID_TYPE_2, ASTEROID_TYPE_3]

# Initialize the LED matrix
LEDMatrix.init()

# Initialize pygame's mixer
pygame.mixer.init()
# Load sounds at the beginning of the game
fire_sound = pygame.mixer.Sound("sounds/fireWeapon.wav")
explosion_sound = pygame.mixer.Sound("sounds/retro-explode-2-236688.wav")
ship_hit_sound = pygame.mixer.Sound("sounds/mixkit-explosion-hit-1704.wav")

# Game state
ship_center = Point(WIDTH // 2, HEIGHT // 2)
bullets = []
asteroids = []
ship_angle = 0  # Initial angle of the ship in degrees
hit_count = 0


# Lock for thread-safe modification of game state
state_lock = threading.Lock()
def reset_game():
    global ship_center, ship_angle, bullets, asteroids, hit_count

    # Reset the ship's position and angle
    ship_center = Point(WIDTH // 2, HEIGHT // 2)
    ship_angle = 0
    hit_count = 0

    # Clear bullets and asteroids
    bullets.clear()
    asteroids.clear()

    # Reinitialize the asteroids
    initialize_asteroids()

def display():
    global asteroids, bullets, ship_center, ship_angle

    with state_lock:
        # Clear the display
        LEDMatrix.gfx_set_all(GFX_OFF)

        # Draw the ship
        for y in range(SHIP_SIZE):
            for x in range(SHIP_SIZE):
                if SHIP_GRID[y][x] == 1:
                    part = rotate_point(Point(ship_center.x + (x - 1), ship_center.y + (y - 1)), ship_center, ship_angle)
                    LEDMatrix.gfx_set_px(int(part.x), int(part.y), GFX_ON)

        # Draw the bullets
        for bullet in bullets:
            LEDMatrix.gfx_set_px(int(bullet.x), int(bullet.y), GFX_ON)

        # Draw the asteroids
        for asteroid, _, _, _ in asteroids:
            for p in asteroid:
                LEDMatrix.gfx_set_px(int(p.x), int(p.y), GFX_ON)

        # Update the display
        LEDMatrix.gfx_render()
# Function to draw the ship based on the grid and rotation
def draw_ship():
    global ship_center, ship_angle
    for y in range(SHIP_SIZE):
        for x in range(SHIP_SIZE):
            if SHIP_GRID[y][x] == 1:
                part = Point(ship_center.x + (x - SHIP_SIZE//2), ship_center.y + (y - SHIP_SIZE//2))
                rotated_part = rotate_point(part, ship_center, ship_angle)
                LEDMatrix.gfx_set_px(int(rotated_part.x), int(rotated_part.y), GFX_ON)

# Function to rotate a point around a center
def rotate_point(p, center, angle):
    angle_rad = math.radians(angle)
    s, c = math.sin(angle_rad), math.cos(angle_rad)
    p = Point(p.x - center.x, p.y - center.y)
    new_x = p.x * c - p.y * s
    new_y = p.x * s + p.y * c
    return Point(new_x + center.x, new_y + center.y)


def move_asteroids():
    global asteroids
    with state_lock:
        updated_asteroids = []
        for asteroid, direction_x, direction_y, speed in asteroids:
            moved_asteroid = [wrap_around(Point(p.x + direction_x * speed, p.y + direction_y * speed)) for p in asteroid]
            updated_asteroids.append((moved_asteroid, direction_x, direction_y, speed))
        asteroids = updated_asteroids

def move_ship_forward():
    global ship_center
    direction = Point(math.cos(math.radians(ship_angle)), math.sin(math.radians(ship_angle)))
    ship_center.x += direction.x
    ship_center.y += direction.y
    
    # Wrap around the screen
    ship_center = wrap_around(ship_center)

# Rotate the ship (angle is updated in input_thread)
def rotate_ship(angle_change):
    global ship_angle
    ship_angle += angle_change
    ship_angle %= 360  # Ensure the angle stays within 0-359 degrees

# Function to move bullets
def move_bullets():
    global bullets
    with state_lock:
        bullets = [wrap_around(Point(bullet.x + math.cos(math.radians(ship_angle)), bullet.y + math.sin(math.radians(ship_angle)))) for bullet in bullets]

# Function to fire a bullet from the front of the ship
def fire_bullet():
    bullet_direction = Point(math.cos(math.radians(ship_angle)), math.sin(math.radians(ship_angle)))
    bullet = Point(ship_center.x + bullet_direction.x, ship_center.y + bullet_direction.y)
    with state_lock:
        bullets.append(bullet)
    #Play the fire weapon sound
    fire_sound.play()
    

def check_collisions():
    global asteroids, bullets, hit_count, ship_center

    with state_lock:
        bullets_to_remove = []
        asteroids_to_remove = []
        ship_hit = False

        # Check for bullet collisions with asteroids
        for i, bullet in enumerate(bullets):
            for j, (asteroid, _, _, _) in enumerate(asteroids):
                if any(math.isclose(bullet.x, p.x, abs_tol=0.5) and math.isclose(bullet.y, p.y, abs_tol=0.5) for p in asteroid):
                    bullets_to_remove.append(i)
                    asteroids_to_remove.append(j)
                    hit_count += 1

                    #Play hit asteroid with bullet sound
                    explosion_sound.play()

                    break  # Stop checking this bullet, as it's already collided

        # Check for ship collisions with asteroids
        for asteroid, _, _, _ in asteroids:
            for p in asteroid:
                for y in range(SHIP_SIZE):
                    for x in range(SHIP_SIZE):
                        if SHIP_GRID[y][x] == 1:
                            part = rotate_point(Point(ship_center.x + (x - 1), ship_center.y + (y - 1)), ship_center, ship_angle)
                            if math.isclose(part.x, p.x, abs_tol=0.5) and math.isclose(part.y, p.y, abs_tol=0.5):
                                ship_hit = True
                                break

        # Remove collided bullets and asteroids
        bullets = [bullets[i] for i in range(len(bullets)) if i not in bullets_to_remove]
        asteroids = [asteroids[j] for j in range(len(asteroids)) if j not in asteroids_to_remove]

        # If ship was hit, flash the screen
        if ship_hit:
            flash_screen()

def move_asteroids():
    global asteroids
    with state_lock:
        updated_asteroids = []
        for asteroid, direction_x, direction_y, speed in asteroids:
            moved_asteroid = [Point(p.x + direction_x * speed, p.y + direction_y * speed) for p in asteroid]
            # Keep the asteroid if it is still on the screen
            if any(0 <= p.y <= HEIGHT and 0 <= p.x <= WIDTH for p in moved_asteroid):
                updated_asteroids.append((moved_asteroid, direction_x, direction_y, speed))
        asteroids = updated_asteroids

# Function to flash the screen and display the score
def flash_screen():
    # Load and play the sound ship hit sound
    ship_hit_sound.play()

    LEDMatrix.gfx_set_all(GFX_ON)  # Turn all LEDs on
    LEDMatrix.gfx_render()
    time.sleep(0.1)  # Brief pause for the flash effect
    LEDMatrix.gfx_set_all(GFX_OFF)  # Turn all LEDs off
    LEDMatrix.gfx_render()

    # Display the score
    display_score_alt2()
    
    time.sleep(2)  # Pause to allow the player to see the score
    
    reset_game()
# Function to move asteroids
def move_asteroids():
    global asteroids
    with state_lock:
        updated_asteroids = []
        for asteroid, direction_x, direction_y, speed in asteroids:
            moved_asteroid = [Point(p.x + direction_x * speed, p.y + direction_y * speed) for p in asteroid]
            # Keep the asteroid if it is still on the screen
            if any(0 <= p.y <= HEIGHT and 0 <= p.x <= WIDTH for p in moved_asteroid):
                updated_asteroids.append((moved_asteroid, direction_x, direction_y, speed))
        asteroids = updated_asteroids

# Initialize asteroids
def initialize_asteroids():
    global asteroids
    # Example usage of the Asteroid class, creating an instance of an asteroid. remove this code!
    asteroid = Asteroid(50, 50, 2, 3, AsteroidTypes.MEDIUM, GRID_WIDTH,GRID_HEIGHT)
    print(asteroid)
	
    for _ in range(INITIAL_ASTEROID_COUNT):
        asteroid, direction_x, direction_y, speed = spawn_asteroid()
        asteroids.append((asteroid, direction_x, direction_y, speed))



# Start the game loop
def game_loop():
    while True:
        # Move asteroids
        move_asteroids()

        # Move bullets
        move_bullets()

        # Check for collisions
        check_collisions()

        # Display the game state
        display()

        # Sleep to control frame rate
        time.sleep(0.1)

# Function to handle user inputs
def input_thread():
    global ship_angle
    getch = _Getch()
    while True:
        ch = getch()
        if ch == 'w':  # Move forward
            move_ship_forward()
        elif ch == 'a':  # Rotate left
            rotate_ship(20)
        elif ch == 'd':  # Rotate right
            rotate_ship(-20)
        elif ch == ' ':  # Fire bullet
            fire_bullet()
# Function to spawn a single asteroid at a random position and direction
def spawn_asteroid():
    asteroid_type = random.choice(ASTEROID_TYPES)
    start_x = random.randint(-ASTEROID_SIZE, WIDTH)  # Spawn off-screen
    start_y = random.randint(-ASTEROID_SIZE, HEIGHT)  # Spawn off-screen
    direction_x = random.uniform(-1, 1)  # Random direction
    direction_y = random.uniform(-1, 1)  # Random direction
    speed = random.uniform(0.1, 0.5)  # Random speed
    asteroid = [Point(start_x + x, start_y + y) for y in range(ASTEROID_SIZE) for x in range(ASTEROID_SIZE) if asteroid_type[y][x] == 1]
    return asteroid, direction_x, direction_y, speed

# Function to spawn asteroids continuously
def spawn_asteroids():
    global asteroids
    while True:
        if len(asteroids) < MAX_ASTEROID_COUNT:
            with state_lock:
                asteroid, direction_x, direction_y, speed = spawn_asteroid()
                asteroids.append((asteroid, direction_x, direction_y, speed))
        time.sleep(random.uniform(0.5, 2))
# Initialize asteroids
def initialize_asteroids():
    global asteroids
    for _ in range(INITIAL_ASTEROID_COUNT):
        asteroid, direction_x, direction_y, speed = spawn_asteroid()
        asteroids.append((asteroid, direction_x, direction_y, speed))

def send_matrix_letter(matrix, char_code, font=LCD_FONT):
    send_matrix_shifted_letter(matrix, char_code, char_code, 0, font=font)

def wrap_around(point):
    if point.x < 0:
        point.x = WIDTH
    elif point.x > WIDTH:
        point.x = 0
    if point.y < 0:
        point.y = HEIGHT
    elif point.y > HEIGHT:
        point.y = 0
    return point

def display_score():
    global hit_count

    # Convert hit count to string and display it on the screen
    score_str = f"Score: {hit_count}"
    for letter in range(len(score_str)):
        LEDMatrix.gfx_letter_rotated_90_clockwise(ord(score_str[letter]), (letter%LEDMatrix.MATRIX_WIDTH)*8, ((LEDMatrix.MATRIX_HEIGHT-1) - letter//LEDMatrix.MATRIX_WIDTH)*8 -1)
        LEDMatrix.gfx_render()
        time.sleep(0.2)

def display_score_alt2():
    global hit_count

    # Convert hit count to string and display it on the screen
    score_str = f"Score: {hit_count}"
    char_width = 8  # Width of each character in pixels
    char_height = 8  # Height of each character in pixels

    # Calculate the number of characters that fit in a row
    max_chars_per_row = GRID_WIDTH // char_width

    # Start from the top-left corner
    for index, letter in enumerate(score_str):
        # Calculate the x and y position for each character
        x_pos = (index % max_chars_per_row) * char_width
        y_pos = (index // max_chars_per_row) * char_height

        # Use the rotated function to draw each letter
        LEDMatrix.gfx_letter_rotated_90_clockwise(
            ord(letter),
            x_pos,  # Horizontal position: left to right
            y_pos   # Vertical position: top to bottom
        )
        LEDMatrix.gfx_render()
        time.sleep(0.2)

def display_score_alt():
    global hit_count

    # Convert hit count to string and display it on the screen
    score_str = f"Score: {hit_count}"
    char_width = 8  # Width of each character in pixels
    char_height = 8  # Height of each character in pixels

    # Calculate the number of characters that fit in a row
    max_chars_per_row = GRID_WIDTH // char_width

    for index, letter in enumerate(score_str):
        # Calculate the x and y position for each character
        x_pos = (index % max_chars_per_row) * char_width
        y_pos = (index // max_chars_per_row) * char_height

        # Use the rotated function to draw each letter
        LEDMatrix.gfx_letter_rotated_90_clockwise(
            ord(letter),
            y_pos,  # Horizontal position: left to right
            x_pos   # Vertical position: top to bottom
        )
        LEDMatrix.gfx_render()
        time.sleep(0.2)
def play_sound(file_path):
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing


# Start the threads
threading.Thread(target=input_thread, daemon=True).start()
threading.Thread(target=spawn_asteroids, daemon=True).start()
# Initialize asteroids
initialize_asteroids()


# Start the game loop
game_loop()