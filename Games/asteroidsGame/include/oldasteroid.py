import math
import random
# type: ignore # Importing the AsteroidTypes from the new file
from include.asteroidType import AsteroidType


class Asteroid:
    def __init__(self, x, y, velocity_x, velocity_y, asteroid_type, screen_width, screen_height):
        """Initialize the asteroid with position, velocity, and size."""
        self.x = x
        self.y = y
        # Scale velocity based on type
        self.velocity_x = velocity_x * asteroid_type.value[1]
        self.velocity_y = velocity_y * asteroid_type.value[1]
        self.size = asteroid_type.value[0]  # Set size based on type
        self.radius = asteroid_type.value[0]/2
        self.asteroid_type = asteroid_type
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_destroyed = False

    def move(self):
        """Move the asteroid based on its velocity and apply screen wrapping."""
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Screen wrapping logic
        if self.x < 0:
            self.x = self.screen_width
        elif self.x > self.screen_width:
            self.x = 0

        if self.y < 0:
            self.y = self.screen_height
        elif self.y > self.screen_height:
            self.y = 0

    def check_collision(self, other_object):
        """Check if this asteroid collides with another object (e.g., ship or bullet)."""
        # If the other object has a 'center' attribute (like PlayerShip), use its center's coordinates
        if hasattr(other_object, 'center'):
            other_x = other_object.center.x
            other_y = other_object.center.y
        else:
            other_x = other_object.x
            other_y = other_object.y

        # Calculate distance between the asteroid and the other object
        distance = math.sqrt((self.x - other_x)**2 + (self.y - other_y)**2)

        # Simple circle collision check
        print(self.radius)
        return distance < (self.radius + other_object.radius)

    def split(self):
        """Split the asteroid into smaller ones if it's not already the smallest size."""
        if self.radius > 1:
            new_radius = self.radius - 1
            new_asteroid_type = AsteroidTypes.from_size(new_radius)
            return [
                Asteroid(self.x, self.y, random.uniform(-1, 1), random.uniform(-1, 1),
                         new_asteroid_type, self.screen_width, self.screen_height),
                Asteroid(self.x, self.y, random.uniform(-1, 1), random.uniform(-1, 1),
                         new_asteroid_type, self.screen_width, self.screen_height)
            ]
        else:
            self.is_destroyed = True  # Mark asteroid as destroyed
        return []

    def draw(self, LEDMatrix):
        """Draw the asteroid on the LED matrix based on its size and graphical representation."""
        graphics = self.get_graphics()  # Get the appropriate graphics for this asteroid
        offset_x = int(self.x - len(graphics) // 2)
        offset_y = int(self.y - len(graphics[0]) // 2)

        for i, row in enumerate(graphics):
            for j, pixel in enumerate(row):
                if pixel == 1:
                    # Ensure the pixel coordinates wrap around the screen boundaries
                    draw_x = (offset_x + i) % self.screen_width
                    draw_y = (offset_y + j) % self.screen_height
                    LEDMatrix.gfx_set_px(draw_x, draw_y, GFX_ON)

    def get_graphics(self):
        """Get the graphical representation of the asteroid based on its type."""
        if self.radius == 1:
            return ASTEROID_TYPE_1
        elif self.radius == 2:
            return ASTEROID_TYPE_2
        elif self.radius == 3:
            return ASTEROID_TYPE_3
        else:
            return []

    def __str__(self):
        return f"Asteroid at ({self.x}, {self.y}) with velocity ({self.velocity_x}, {self.velocity_y}) and size {self.size}"


