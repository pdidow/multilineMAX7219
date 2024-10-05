from dataclasses import dataclass
import random
from include.asteroidType import AsteroidType
from include.playerShip import PlayerShip
from include.bullet import Bullet
from math import sqrt

def get_bounding_box(x, y, width, height):
    """Calculate the bounding box given position, width, and height."""
    return {
        'x1': x,
        'y1': y,
        'x2': x + width,
        'y2': y + height
}

@dataclass
class Asteroid:
    x: float
    y: float
    velocity_x: float
    velocity_y: float
    asteroid_type: AsteroidType
    screen_width: int
    screen_height: int
    is_destroyed: bool = False

    def __post_init__(self):
        """Initialize asteroid-specific properties after the default dataclass initialization."""
        self.speed_multiplier = self.asteroid_type.get_speed_multiplier() * 0.5  # Reduce speed multiplier to half
        self.velocity_x *= self.speed_multiplier
        self.velocity_y *= self.speed_multiplier
        self.graphic = self.asteroid_type.get_graphic()
        self.width = len(self.graphic[0])
        self.height = len(self.graphic)

    def move(self):
        """Move the asteroid and wrap around the screen edges in smaller steps."""
        steps = 2  # Split movement into smaller steps
        for _ in range(steps):
            self.x += self.velocity_x / steps
            self.y += self.velocity_y / steps

            # Screen wrapping logic for 32x24 LED matrix
            if self.x < 0:
                 self.x = self.screen_width - 1  # Wrap around to the right edge
            elif self.x >= self.screen_width:
                self.x = 0  # Wrap around to the left edge

            if self.y < 0:
                self.y = self.screen_height - 1  # Wrap around to the bottom edge
            elif self.y >= self.screen_height:
                self.y = 0  # Wrap around to the top edge

    def check_collision(self, other_object):
        """Check if the asteroid collides with the player ship or a bullet using bounding box collision detection."""

        # Calculate bounding box for the asteroid
        asteroid_box = {
            'x1': self.x,
            'y1': self.y,
            'x2': self.x + self.width,
            'y2': self.y + self.height
        }

        if isinstance(other_object, PlayerShip):
            # Calculate bounding box for the player ship
            ship_box = {
                'x1': other_object.center.x - other_object.size // 2,
                'y1': other_object.center.y - other_object.size // 2,
                'x2': other_object.center.x + other_object.size // 2,
                'y2': other_object.center.y + other_object.size // 2
            }

            # Check bounding box overlap
            if self._bounding_box_overlap(asteroid_box, ship_box):
                # Optional: Check pixel-perfect collision
                return self._pixel_perfect_collision(other_object.ship_grid, asteroid_box, ship_box)

        elif isinstance(other_object, Bullet):
            # Calculate bounding box for the bullet (assuming it's a point)
            bullet_box = {
                'x1': other_object.x,
                'y1': other_object.y,
                'x2': other_object.x + other_object.radius * 2,  # Radius might be 0 or small value
                'y2': other_object.y + other_object.radius * 2
            }

            # Check bounding box overlap
            if self._bounding_box_overlap(asteroid_box, bullet_box):
                return True  # Simple bounding box collision for bullets

        return False  # No collision if it's an unhandled object type

    def _bounding_box_overlap(self, box1, box2):
        """Check if two bounding boxes overlap."""
        return (box1['x1'] < box2['x2'] and box1['x2'] > box2['x1'] and
                box1['y1'] < box2['y2'] and box1['y2'] > box2['y1'])

    def _pixel_perfect_collision(self, ship_grid, asteroid_box, ship_box):
        """Check pixel-perfect collision between the ship grid and the asteroid graphic."""
        # Convert bounding box coordinates to integers and clamp within matrix boundaries
        x1 = max(0, min(int(max(ship_box['x1'], asteroid_box['x1'])), self.screen_width - 1))
        x2 = max(0, min(int(min(ship_box['x2'], asteroid_box['x2'])), self.screen_width - 1))
        y1 = max(0, min(int(max(ship_box['y1'], asteroid_box['y1'])), self.screen_height - 1))
        y2 = max(0, min(int(min(ship_box['y2'], asteroid_box['y2'])), self.screen_height - 1))

        # Iterate over the overlapping area
        for x in range(x1, x2):
            for y in range(y1, y2):
                # Translate the coordinates to the ship and asteroid grids
                ship_x = x - int(ship_box['x1'])
                ship_y = y - int(ship_box['y1'])
                asteroid_x = x - int(asteroid_box['x1'])
                asteroid_y = y - int(asteroid_box['y1'])

                # Ensure the indices are within bounds of both grids
                if (0 <= ship_y < len(ship_grid) and
                    0 <= ship_x < len(ship_grid[0]) and
                    0 <= asteroid_y < len(self.graphic) and
                    0 <= asteroid_x < len(self.graphic[0])):
                
                    # Check if both the ship and asteroid have a pixel at this position
                    if (ship_grid[ship_y][ship_x] == 1 and
                        self.graphic[asteroid_y][asteroid_x] == 1):
                        return True  # Pixel-perfect collision detected

        return False  # No pixel-perfect collision detected


    
    
    def _bounding_box_collision(self, other_object):
        """Check Collisions using bounding box."""
        # Check if colliding with the player ship
        if isinstance(other_object, PlayerShip):
            # Add bounding box collision logic for ship if necessary
            pass
        
        # Check if colliding with a bullet
        elif isinstance(other_object, Bullet):
            # Add bounding box collision logic for bullet if necessary
            pass
        
        return False  # No collision if it's an unhandled object type

    def split(self):
            """Split the asteroid into smaller asteroids if possible."""
            if self.asteroid_type == AsteroidType.SMALL:
                self.is_destroyed = True
                return []

            # Determine the new type for the split asteroids
            new_type = AsteroidType.MEDIUM if self.asteroid_type == AsteroidType.LARGE else AsteroidType.SMALL
        
            # Calculate new velocities for split asteroids
            new_velocity_1 = (self.velocity_x + random.uniform(-1, 1), self.velocity_y + random.uniform(-1, 1))
            new_velocity_2 = (self.velocity_x + random.uniform(-1, 1), self.velocity_y + random.uniform(-1, 1))
        
            # Normalize velocities to ensure they move away in opposite directions
            new_velocity_1 = self._normalize_velocity(new_velocity_1)
            new_velocity_2 = self._normalize_velocity(new_velocity_2)
        
            # Create exactly two smaller asteroids with the new velocities
            return [
                Asteroid(self.x, self.y, new_velocity_1[0], new_velocity_1[1], 
                         new_type, self.screen_width, self.screen_height),
                Asteroid(self.x, self.y, new_velocity_2[0], new_velocity_2[1], 
                         new_type, self.screen_width, self.screen_height)
            ]

    def _normalize_velocity(self, velocity):
            """Normalize the given velocity vector to keep consistent speed."""
            vx, vy = velocity
            speed = sqrt(vx ** 2 + vy ** 2)
            if speed == 0:
                return (vx, vy)  # Avoid division by zero
            return (vx / speed * self.speed_multiplier, vy / speed * self.speed_multiplier)

    def draw(self, LEDMatrix):
        """Draw the asteroid on the LED matrix."""
        offset_x = int(self.x - self.width // 2)
        offset_y = int(self.y - self.height // 2)

        for i, row in enumerate(self.graphic):
            for j, pixel in enumerate(row):
                if pixel == 1:
                    draw_x = (offset_x + j) % self.screen_width
                    draw_y = (offset_y + i) % self.screen_height
                    LEDMatrix.gfx_set_px(draw_x, draw_y, LEDMatrix.GFX_ON)

    def __str__(self):
        return f"Asteroid at ({self.x}, {self.y}) with velocity ({self.velocity_x}, {self.velocity_y}) and type {self.asteroid_type.name}"
