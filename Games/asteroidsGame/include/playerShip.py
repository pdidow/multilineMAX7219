import math
import time
import pygame

import multilineMAX7219 as LEDMatrix

# Import fonts
from multilineMAX7219_fonts import CP437_FONT, SINCLAIRS_FONT, LCD_FONT, TINY_FONT
from multilineMAX7219 import GFX_ON, GFX_OFF, GFX_INVERT
from multilineMAX7219 import send_matrix_letter

from include.point import Point
from include.bullet import Bullet
import threading


class PlayerShip:

    def __init__(self, center, size):
        self.center = center  # The position of the ship
        self.size = size  # Size of the ship
        self.ship_angle = 0.0  # Initial angle of the ship
        self.radius = size / 2  # Use the ship's size to define its radius
        self.bullet_speed = 1
        self.hit_count = 0  # Initialize hit_count as an instance variable
        self.score = 0
        # init empty list of player's bullets. This list will contain instances of the Bullet class.
        self.bullets = []
        self.bulletlifespan = 100
        self.lives = 3
        self.ship_grid = [
            [0, 1, 0, 0],
            [0, 1, 1, 1],
            [0, 1, 1, 1],
            [0, 1, 0, 0]
        ]
        # Initialize sounds
        self.fire_sound = pygame.mixer.Sound("sounds/fireWeapon.wav")
        self.ship_hit_sound = pygame.mixer.Sound(
            "sounds/mixkit-explosion-hit-1704.wav")
        # Lock for thread-safe modification of game state
        self.state_lock = threading.Lock()

    def rotate_ship(self, angle_change):
        """Rotate the ship by changing its angle."""
        self.ship_angle = (self.ship_angle +
                           angle_change) % 360  # Keep angle between 0 and 360

    def move_ship_forward(self):
        """Move the ship forward based on its current angle."""
        direction_x = math.cos(math.radians(self.ship_angle))
        direction_y = math.sin(math.radians(self.ship_angle))
        self.center.x += direction_x
        self.center.y += direction_y
        self.center = self.wrap_around(
            self.center)  # Ensure it stays on screen

    def move_bullets(self):
        """Move bullets, wrap them around the screen, and remove expired bullets."""
        with self.state_lock:
            new_bullets = []
            for bullet in self.bullets:
                # Update the bullet's position and lifespan
                bullet.update_position()

                # Wrap the bullet around the screen if necessary
                wrapped_bullet = self.wrap_around(Point(bullet.x, bullet.y))
                bullet.x = wrapped_bullet.x
                bullet.y = wrapped_bullet.y

                # Only keep the bullet if it hasn't expired
                if bullet.lifespan > 0:
                    new_bullets.append(bullet)

            self.bullets = new_bullets

    def flash_screen(self):
        """Flash the screen and display the score when the ship is hit."""
        # Load and play the sound ship hit sound
        self.ship_hit_sound.play()

        LEDMatrix.gfx_set_all(GFX_ON)  # Turn all LEDs on
        LEDMatrix.gfx_render()
        time.sleep(0.1)  # Brief pause for the flash effect
        LEDMatrix.gfx_set_all(GFX_OFF)  # Turn all LEDs off
        LEDMatrix.gfx_render()

        # Display the score on the screen
        self.display_score()

        time.sleep(2)  # Pause to allow the player to see the score

        # Reset the game state after displaying the score
        #reset_game()

    def display_score(self):
      
        """Display the score based on hit_count."""
        LEDMatrix.gfx_set_all(GFX_OFF)  # Clear the display
        LEDMatrix.gfx_render()  # Render the cleared state
    
        score_str = f"Score: {self.score}"  
        for letter in score_str:
            send_matrix_letter(LEDMatrix, ord(letter), font=LCD_FONT)
            time.sleep(0.1)  # Delay between characters
    
        LEDMatrix.gfx_render()  # Render the updated display with the score
    

       
    
    def destroy(self):
        """Handle the destruction of the player's ship."""
        # Play the ship's destruction sound
        self.ship_hit_sound.play()

        # Mark the ship as destroyed (you can add a flag if needed)
        self.lives -= 1

        # Reset the ship's position (you can adjust this as needed)
        # Example: reset to the center of the screen
        self.center = Point(16, 12)  # Adjust as necessary
        # Clear all bullets
        with self.state_lock:
            self.bullets = []  # Clear the list of bullets
        print("Ship destroyed!")
        self.display_score()

    def fire_bullet(self):
        """Fire a bullet from the front of the ship."""
        # Calculate the bullet direction based on the ship's angle
        bullet_angle = self.ship_angle
        bullet_direction = Point(
            math.cos(math.radians(bullet_angle)),
            math.sin(math.radians(bullet_angle))
        )

        # Set the initial position of the bullet at the front of the ship
        bullet_start_x = self.center.x + bullet_direction.x * self.size
        bullet_start_y = self.center.y + bullet_direction.y * self.size

        # Calculate bullet velocity based on the direction and bullet speed
        velocity_x = bullet_direction.x * self.bullet_speed
        velocity_y = bullet_direction.y * self.bullet_speed

        # Create the bullet with the starting position and velocity
        bullet = Bullet(bullet_start_x, bullet_start_y, velocity_x,
                        velocity_y, bullet_angle, self.bulletlifespan)

        # Add the bullet to the ship's list of bullets
        self.bullets.append(bullet)

        # Play the fire sound
        self.fire_sound.play()

        return bullet  # Return the bullet to be tracked in the game loop

    def wrap_around(self, point):
        """Ensure the ship or a point wraps around the screen."""
        WIDTH = 32  # Matrix width should be a constant or part of settings
        HEIGHT = 24  # Matrix height
        if point.x < 0:
            point.x = WIDTH
        elif point.x > WIDTH:
            point.x = 0
        if point.y < 0:
            point.y = HEIGHT
        elif point.y > HEIGHT:
            point.y = 0
        return point

    def draw(self):
        """Draw the ship on the LED matrix based on its position and angle."""
        for y in range(self.size):
            for x in range(self.size):
                if self.ship_grid[y][x] == 1:
                    # Rotate each ship part and draw on the matrix
                    rotated_point = self.rotate_point(
                        Point(self.center.x + (x - 1), self.center.y + (y - 1)))
                    LEDMatrix.gfx_set_px(int(rotated_point.x), int(
                        rotated_point.y), LEDMatrix.GFX_ON)
        LEDMatrix.gfx_render()

    


    def rotate_point(self, point):
        """Rotate a point around the ship's center."""
        s = math.sin(math.radians(self.ship_angle))
        c = math.cos(math.radians(self.ship_angle))

        # Translate point back to origin:
        translated_x = point.x - self.center.x
        translated_y = point.y - self.center.y

        # Rotate point
        rotated_x = translated_x * c - translated_y * s
        rotated_y = translated_x * s + translated_y * c

        # Translate point back
        point.x = rotated_x + self.center.x
        point.y = rotated_y + self.center.y

        return point
