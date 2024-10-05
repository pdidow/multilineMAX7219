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
from include.ufo import UFO

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
        

        # Update the display
        LEDMatrix.gfx_render()


def reset_asteroidField():
    global asteroids
    # Clear existing asteroids
    asteroidField.clear()
    # Spawn the initial batch of asteroids
    for _ in range(INITIAL_ASTEROID_COUNT):
        asteroid, direction_x, direction_y, speed = spawn_asteroid()
        asteroidField.append((asteroid, direction_x, direction_y, speed))

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

def display_score(score):
        """Display the player's score on the LED matrix or console."""
        # Assuming there is a method to send text to the LEDMatrix
        # Replace the print statement with your actual implementation to render the score
        print(f"Score: {score}")  # For debugging, print to the console

# Start the game loop
def game_loop():
    global asteroid_field  # Declare asteroid_field as global here

    # Initialize Pygame for sound
    pygame.init()
    pygame.mixer.init()

    # Load sounds at the beginning of the game
    small_explosion_sound = pygame.mixer.Sound("sounds/bangSmall.wav")
    medium_explosion_sound = pygame.mixer.Sound("sounds/bangMedium.wav")
    large_explosion_sound = pygame.mixer.Sound("sounds/bangLarge.wav")
    largeUFO_sound = pygame.mixer.Sound("sounds/saucerBig.wav")
    smallUFO_sound = pygame.mixer.Sound("sounds/saucerSmall.wav")


    asteroid_field = AsteroidField()  # Create our asteroidField object
    asteroid_field.populate(1, GRID_WIDTH, GRID_HEIGHT, ship)  # Populate the field with asteroids at the start of the game.
    # Initialize the UFO (for example, a large UFO)
    lufo = UFO('large', GRID_WIDTH, GRID_HEIGHT)

    while True:
        # Move asteroids
        asteroid_field.move_asteroids()

        # Move the UFO
        if lufo.is_alive:
            lufo.move()
            largeUFO_sound.play()


        # Move bullets
        ship.move_bullets()

        # Check for collisions
        asteroid_field.check_ship_collision(ship)  # Check if the ship collides with any asteroids
        asteroid_field.check_bullet_collisions(ship, small_explosion_sound, medium_explosion_sound, large_explosion_sound)  # Check if bullets hit any asteroids
        
        # Check for UFO bullet firing
        ufo_bullet = None
        if lufo.is_alive:
            ufo_bullet = lufo.fire_bullet(ship.center)  # UFO fires at the player's ship

        if ufo_bullet:
            # Add UFO bullet to the game (store and display it like ship's bullets)
            pass

        # Check for collisions
        asteroid_field.check_ship_collision(ship)  # Check if the ship collides with any asteroids
        asteroid_field.check_bullet_collisions(ship, small_explosion_sound, medium_explosion_sound, large_explosion_sound)  # Check if bullets hit any asteroids

        # Check if UFO is hit by player's bullets
        if lufo.is_alive:
            if lufo.check_collision(ship.bullets):
                # Play explosion sound or add points if needed
                lufo.is_alive = False  # Destroy the UFO
                # Optional: Play sound
                pygame.mixer.Sound(large_explosion_sound).play()

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
            asteroid_field.start_next_level(GRID_WIDTH, GRID_HEIGHT, ship)

        # Update and play heartbeat sound based on asteroid count
        asteroid_field.update_heartbeat()

        # Display the game state (rendering the asteroids, ship, bullets, etc.)
        display()

        # Display the UFO on the LED matrix if alive
        if lufo.is_alive:
            lufo.draw(LEDMatrix)  # Draw the UFO on the LEDMatrix

        # Display the score
        display_score(ship.score)

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
