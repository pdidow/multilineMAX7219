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
from include.playerShip import PlayerShip
from include.asteroidField import AsteroidField
from include.point import Point
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
import time
from luma.core.legacy import text
from luma.core.legacy.font import TINY_FONT


# Constants
WIDTH = 8 * LEDMatrix.MATRIX_WIDTH - 1
HEIGHT = 8 * LEDMatrix.MATRIX_HEIGHT - 1
SHIP_SIZE = 4
ASTEROID_SIZE = 4
INITIAL_ASTEROID_COUNT = 5
MAX_ASTEROID_COUNT = 10
MAX_BULLETS = 3  # no more than 3 player bullets alive at a time
GRID_WIDTH = 32
GRID_HEIGHT = 24

# Initialize the LED matrix
LEDMatrix.init()


# Game state
# instantiate ship etc
ship = PlayerShip(Point(WIDTH // 2, HEIGHT // 2), SHIP_SIZE)
hit_count = 0

# Lock for thread-safe modification of game state
state_lock = threading.Lock()
# Declare asteroid_field globally
asteroid_field = None


def reset_game():
    global bullets, asteroids, hit_count

    # Reset the ship's position and angle
    ship.center = Point(WIDTH // 2, HEIGHT // 2)
    ship.ship_angle = 0
    hit_count = 0

    # Clear bullets and asteroids
    bullets.clear()
    asteroidField.clear()

    # Reinitialize the asteroids
    reset_asteroidField()


def display():
    global asteroid_field, bullets

    with state_lock:
        # Clear the display
        LEDMatrix.gfx_set_all(GFX_OFF)

        # Draw the ship
        ship.draw()
        # Draw the bullets
        for bullet in ship.bullets:
            LEDMatrix.gfx_set_px(int(bullet.x), int(bullet.y), GFX_ON)

        
        # Draw the asteroids using the asteroid's own draw method
        for asteroid in asteroid_field.asteroids:
            asteroid.draw(LEDMatrix)
        # LEDMatrix.gfx_set_px(int(x), int(y), GFX_ON)

        # Update the display
        LEDMatrix.gfx_render()

# Function to display static text on the LED matrix
def display_text(device, text_to_display, font):
    with canvas(device) as draw:
        # Display the text in a fixed position, adjust (x, y) if needed
        text(draw, (0, 2), text_to_display, fill="white", font=font)

def reset_asteroidField():
    global asteroids
    # Clear existing asteroids
    asteroidField.clear()
    # Spawn the initial batch of asteroids
    for _ in range(INITIAL_ASTEROID_COUNT):
        asteroid, direction_x, direction_y, speed = spawn_asteroid()
        asteroidField.append((asteroid, direction_x, direction_y, speed))


def check_collisions():
    global asteroidField, bullets, hit_count
    with state_lock:
        bullets_to_remove = []
        asteroids_to_remove = []
        ship.ship_hit = False

        # Check for bullet collisions with asteroids
        for i, bullet in enumerate(ship.bullets):
            for j, (asteroid, _, _, _) in enumerate(asteroidField):
                if any(
                    math.isclose(bullet.x, p.x, abs_tol=0.5)
                    and math.isclose(bullet.y, p.y, abs_tol=0.5)
                    for p in asteroid.get_graphics()
                ):
                    bullets_to_remove.append(i)
                    asteroids_to_remove.append(j)
                    hit_count += 1

                    # Play hit asteroid with bullet sound
                    explosion_sound.play()

                    break  # Stop checking this bullet, as it's already collided

        # Check for ship collisions with asteroids
        for asteroid, _, _, _ in asteroidField:
            for p in asteroid.get_graphics():
                for y in range(SHIP_SIZE):
                    for x in range(SHIP_SIZE):
                        if ship.ship_grid[y][x] == 1:
                            part = ship.rotate_point(
                                Point(ship.center.x + (x - 1), ship.center.y + (y - 1))
                            )
                            if math.isclose(part.x, p.x, abs_tol=0.5) and math.isclose(
                                part.y, p.y, abs_tol=0.5
                            ):
                                ship.ship_hit = True
                                break
        # Remove collided bullets and asteroids
        ship.bullets = [
            ship.bullets[i]
            for i in range(len(ship.bullets))
            if i not in bullets_to_remove
        ]
        asteroidField = [
            asteroidField[j]
            for j in range(len(asteroidField))
            if j not in asteroids_to_remove
        ]

        # If ship was hit, flash the screen
        if ship.ship_hit:
            flash_screen()


# Function to flash the screen and display the score
def flash_screen():
    # Load and play the sound ship hit sound
    ship.ship_hit_sound.play()

    LEDMatrix.gfx_set_all(GFX_ON)  # Turn all LEDs on
    LEDMatrix.gfx_render()
    time.sleep(0.1)  # Brief pause for the flash effect
    LEDMatrix.gfx_set_all(GFX_OFF)  # Turn all LEDs off
    LEDMatrix.gfx_render()

    # Display the score
    display_score()

    time.sleep(2)  # Pause to allow the player to see the score

    reset_game()


def move_asteroids():
    with state_lock:
        for asteroid in asteroid_field:
            # Move each asteroid based on its velocity
            asteroid.move()

            # Wrap around the screen if necessary
            if asteroid.x < 0:
                asteroid.x = asteroid.screen_width
            elif asteroid.x > asteroid.screen_width:
                asteroid.x = 0

            if asteroid.y < 0:
                asteroid.y = asteroid.screen_height
            elif asteroid.y > asteroid.screen_height:
                asteroid.y = 0


# Function to handle user inputs
def input_thread():
    getch = _Getch()
    while True:
        ch = getch()
        if ch == "w":  # Move forward
            ship.move_ship_forward()
        elif ch == "a":  # Rotate left
            ship.rotate_ship(20)
        elif ch == "d":  # Rotate right
            ship.rotate_ship(-20)
        elif ch == " ":  # Fire bullet
            fire_bullet()



# Function to fire a bullet from the front of the ship
def fire_bullet():
    bullet = ship.fire_bullet()  # Use the ship's method to fire a bullet
    with state_lock:
        ship.bullets.append(bullet)


# Function to spawn asteroids continuously
def update_asteroidField():
    while True:
        if len(asteroidField) < MAX_ASTEROID_COUNT:
            with state_lock:
                asteroid, direction_x, direction_y, speed = spawn_asteroid()
                asteroidField.append((asteroid, direction_x, direction_y, speed))
        time.sleep(random.uniform(0.5, 2))


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
        char = score_str[letter]
        send_matrix_letter(LEDMatrix, ord(char), font=LCD_FONT)
        time.sleep(0.1)  # Delay between characters


# Start the game loop
def game_loop():
    global asteroid_field  # Declare asteroid_field as global here

    # Initialize Pygame for sound
    pygame.init()
    pygame.mixer.init()
    # Load sounds at the beginning of the game
    explosion_sound = pygame.mixer.Sound("sounds/retro-explode-2-236688.wav")
    # Set up the LED matrix
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=12, block_orientation=-90, rotate=2, width=32, height=24)  # Adjust parameters as needed

    #Display game title for 5 sec    
    display_text(device, "Asteroids!", TINY_FONT)
    # Hold the text on the display for 5 seconds (adjust as needed)
    time.sleep(5)

    # Clear the LED matrix after the delay
    device.clear()


    asteroid_field = AsteroidField()  # Create our asteroidField object
    asteroid_field.populate(
        1, GRID_WIDTH, GRID_HEIGHT, ship
    )  # Populate the field with 4 asteroids at the start of the game.

    while True:
        # Move asteroids
        asteroid_field.move_asteroids()

        # Move bullets
        ship.move_bullets()

        # Check for collisions
        asteroid_field.check_ship_collision(
            ship
        )  # Check if the ship collides with any asteroids
        asteroid_field.check_bullet_collisions(
            ship
        )  # Check if bullets hit any asteroids
        
         # Split asteroids if needed
        new_asteroids = []
        for asteroid in asteroid_field.asteroids:
            if asteroid.is_destroyed:
                new_asteroids.extend(asteroid.split())
        
        # Add the new split asteroids to the asteroid field
        asteroid_field.asteroids.extend(new_asteroids)

        # Remove destroyed asteroids
        asteroid_field.remove_destroyed_asteroids()

        # If no asteroids left, start the next level
        if len(asteroid_field.asteroids) == 0:
            asteroid_field.start_next_level(GRID_WIDTH,GRID_HEIGHT, ship)
            
        # Update and play heartbeat sound based on asteroid count
        asteroid_field.update_heartbeat()

        # Display the game state (rendering the asteroids, ship, bullets, etc.)
        display()

        # Control frame rate using pygame's built-in timing
        pygame.time.delay(200)  # Delay 100 ms for approx. 10 FPS (adjust as needed)

    # Quit Pygame after the game loop ends
    pygame.quit()


if __name__ == "__main__":
    # Start the input thread
    threading.Thread(target=input_thread, daemon=True).start()

    # Start the asteroid spawn thread
    # threading.Thread(target=update_asteroidField, daemon=True).start()

    # Start the main game loop
    game_loop()
