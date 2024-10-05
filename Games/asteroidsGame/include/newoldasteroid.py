import random
from include.asteroidType import AsteroidType, get_random_asteroid_type

def get_bounding_box(x, y, width, height):
    """Calculate the bounding box given position, width, and height."""
    x_min = x
    y_min = y
    x_max = x + width
    y_max = y + height
    return (x_min, y_min, x_max, y_max)

class Asteroid:
    def __init__(self, x, y, velocity_x, velocity_y, asteroid_type: AsteroidType, screen_width, screen_height):
        """Initialize the asteroid with position, velocity, and size based on type."""
        self.x = x
        self.y = y
        self.asteroid_type = asteroid_type
        self.speed_multiplier = self.asteroid_type.get_speed_multiplier()  # Use it as a method
        self.velocity_x = velocity_x * speed_multiplier
        self.velocity_y = velocity_y * speed_multiplier
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_destroyed = False
        self.graphic = asteroid_type.get_graphic()
        self.width = len(self.graphic[0])  # Width of the asteroid based on graphic
        self.height = len(self.graphic)     # Height of the asteroid based on graphic

    def move(self):
        """Move the asteroid and wrap around the screen edges."""
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
        """Check if the asteroid collides with another object."""
        # Get the bounding box for the asteroid
        asteroid_bb = self.get_bounding_box()

        # Get the bounding box for the other object
        other_x = other_object['x']
        other_y = other_object['y']
        other_width = other_object['width']
        other_height = other_object['height']
        other_bb = get_bounding_box(other_x, other_y, other_width, other_height)

        # Check for bounding box overlap
        if (asteroid_bb[2] < other_bb[0] or asteroid_bb[0] > other_bb[2] or
                asteroid_bb[3] < other_bb[1] or asteroid_bb[1] > other_bb[3]):
            return False  # No bounding box overlap, no collision

        # Bounding boxes overlap, now check for pixel-by-pixel collision
        for i in range(self.height):
            for j in range(self.width):
                if self.graphic[i][j] == 1:
                    asteroid_x = self.x + j
                    asteroid_y = self.y + i

                    # Check if this pixel is within the other object's bounding box
                    if (other_bb[0] <= asteroid_x <= other_bb[2] and 
                        other_bb[1] <= asteroid_y <= other_bb[3]):
                        return True  # Collision detected

        return False  # No collision

    def get_bounding_box(self):
        """Calculate the bounding box for the asteroid."""
        return get_bounding_box(self.x, self.y, self.width, self.height)

    def split(self):
        """Split the asteroid into smaller ones."""
        if self.asteroid_type == AsteroidType.SMALL:
            self.is_destroyed = True
            return []

        new_size = [AsteroidType.SMALL, AsteroidType.MEDIUM][[AsteroidType.MEDIUM, AsteroidType.LARGE].index(self.asteroid_type)]
        return [
            Asteroid(self.x, self.y, random.uniform(-1, 1), random.uniform(-1, 1), 
                     new_size, self.screen_width, self.screen_height),
            Asteroid(self.x, self.y, random.uniform(-1, 1), random.uniform(-1, 1), 
                     new_size, self.screen_width, self.screen_height)
        ]

    def draw(self, LEDMatrix):
        """Draw the asteroid on the LED matrix based on its type's graphic."""
        graphics = self.graphic
        offset_x = int(self.x - len(graphics) // 2)
        offset_y = int(self.y - len(graphics[0]) // 2)

        for i, row in enumerate(graphics):
            for j, pixel in enumerate(row):
                if pixel == 1:
                    # Wrap around screen boundaries
                    draw_x = (offset_x + j) % self.screen_width
                    draw_y = (offset_y + i) % self.screen_height
                    LEDMatrix.gfx_set_px(draw_x, draw_y, GFX_ON)

    def __str__(self):
        return f"Asteroid at ({self.x}, {self.y}) with velocity ({self.velocity_x}, {self.velocity_y}) and type {self.asteroid_type.name}"
