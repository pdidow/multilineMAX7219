import random

GFX_ON = 1  # Constant to turn on a pixel

class Asteroid:
    def __init__(self, x, y, size, asteroid_type, direction, speed):
        self.x = x  # X position of the asteroid
        self.y = y  # Y position of the asteroid
        self.size = size  # "large", "medium", "small"
        self.asteroid_type = asteroid_type  # 0 = TYPE_1, 1 = TYPE_2, 2 = TYPE_3
        self.direction = direction  # Direction in which the asteroid is moving
        self.speed = speed  # Speed of the asteroid
        self.is_destroyed = False  # If true, the asteroid is marked for destruction

    def update(self):
        """Update the asteroid's position based on its speed and direction."""
        self.x += self.speed * self.direction[0]  # Update x position
        self.y += self.speed * self.direction[1]  # Update y position

    def draw(self, LEDMatrix):
        """Draw the asteroid on the LED matrix based on its type and size."""
        size_multiplier = self.size_to_multiplier(self.size)

        # Select the asteroid type and draw the corresponding shape
        if self.asteroid_type == 0:
            self.draw_TYPE_1(LEDMatrix, size_multiplier)
        elif self.asteroid_type == 1:
            self.draw_TYPE_2(LEDMatrix, size_multiplier)
        elif self.asteroid_type == 2:
            self.draw_TYPE_3(LEDMatrix, size_multiplier)

    def size_to_multiplier(self, size):
        """Convert the asteroid size to a size multiplier for scaling the shape."""
        if size == "large":
            return 3
        elif size == "medium":
            return 2
        elif size == "small":
            return 1

    def draw_TYPE_1(self, LEDMatrix, multiplier):
        """Draw the TYPE_1 asteroid pattern."""
        pattern = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        self.draw_pattern(LEDMatrix, pattern, multiplier)

    def draw_TYPE_2(self, LEDMatrix, multiplier):
        """Draw the TYPE_2 asteroid pattern."""
        pattern = [(0, 0), (2, 0), (-2, 0), (0, 2), (0, -2), (1, 1), (-1, 1)]
        self.draw_pattern(LEDMatrix, pattern, multiplier)

    def draw_TYPE_3(self, LEDMatrix, multiplier):
        """Draw the TYPE_3 asteroid pattern."""
        pattern = [(0, 0), (1, 0), (-1, 0), (1, 1), (-1, 1), (0, 1), (0, -1), (2, 0), (-2, 0)]
        self.draw_pattern(LEDMatrix, pattern, multiplier)

    def draw_pattern(self, LEDMatrix, pattern, multiplier):
        """Helper function to draw a pattern on the LED matrix, scaled by multiplier."""
        for dx, dy in pattern:
            for scale_x in range(multiplier):
                for scale_y in range(multiplier):
                    LEDMatrix.gfx_set_px(int(self.x + dx * multiplier + scale_x), int(self.y + dy * multiplier + scale_y), GFX_ON)

    def split(self):
        """Split the asteroid into smaller ones when destroyed."""
        if self.size == "large":
            return [Asteroid(self.x, self.y, "medium", self.asteroid_type, random_direction(), self.speed)]
        elif self.size == "medium":
            return [Asteroid(self.x, self.y, "small", self.asteroid_type, random_direction(), self.speed)]
        else:
            self.is_destroyed = True
            return []

class AsteroidField:
    def __init__(self, num_asteroids):
        self.asteroids = []
        for _ in range(num_asteroids):
            size = random.choice(["large", "medium", "small"])
            asteroid_type = random.randint(0, 2)
            x = random.randint(0, 128)  # Assuming 128x64 LED matrix
            y = random.randint(0, 64)
            direction = random_direction()
            speed = random.uniform(0.5, 2.0)
            self.asteroids.append(Asteroid(x, y, size, asteroid_type, direction, speed))

    def update(self):
        """Update all asteroids' positions and remove destroyed ones."""
        for asteroid in self.asteroids:
            asteroid.update()
        self.asteroids = [asteroid for asteroid in self.asteroids if not asteroid.is_destroyed]

    def draw(self, LEDMatrix):
        """Draw all asteroids on the LED matrix."""
        for asteroid in self.asteroids:
            asteroid.draw(LEDMatrix)

    def handle_collisions(self, bullets):
        """Handle asteroid-bullet collisions."""
        for asteroid in self.asteroids[:]:
            for bullet in bullets:
                if self.check_collision(asteroid, bullet):
                    bullets.remove(bullet)
                    new_asteroids = asteroid.split()
                    self.asteroids.remove(asteroid)
                    self.asteroids.extend(new_asteroids)

    def check_collision(self, asteroid, bullet):
        """Check if a bullet has collided with an asteroid."""
        distance = ((asteroid.x - bullet.x)**2 + (asteroid.y - bullet.y)**2)**0.5
        return distance < 2  # Collision if close enough

def random_direction():
    """Generate a random direction vector."""
    return [random.uniform(-1, 1), random.uniform(-1, 1)]
