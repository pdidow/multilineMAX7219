import time
import random
import pygame
from include.asteroid import Asteroid
from include.asteroidType import AsteroidType, get_random_asteroid_type
from math import sqrt
from include.point import Point
GRID_WIDTH = 32
GRID_HEIGHT = 24

# Initialize pygame's mixer for sound
pygame.mixer.init()


class AsteroidField:
    def __init__(self):
        self.asteroids = []  # Collection of Asteroid objects
        self.heartbeat_interval = 2  # Start with a 2-second interval for the heartbeat sound
        # Track the last time the heartbeat played
        self.last_heartbeat_time = time.time()

        # Load the heartbeat sounds using pygame
        self.heartbeat1_sound = pygame.mixer.Sound('sounds/beat1.wav')
        self.heartbeat2_sound = pygame.mixer.Sound('sounds/beat2.wav')
        self.level = 1
        self.asteroid_count = 0

    def populate(self, count, screen_width, screen_height, ship):
            """Populate the asteroid field with a specific number of large asteroids,
            ensuring they are not too close to the player's ship."""
            self.clear()  # Clear existing asteroids
            self.asteroid_count = count
            min_safe_distance = 10  # Minimum distance from ship to asteroid

            for _ in range(count):
                # Generate random position for the asteroid
                while True:
                    x = random.uniform(0, screen_width)
                    y = random.uniform(0, screen_height)

                    # Calculate the distance from the ship's position
                    distance_from_ship = sqrt((x - ship.center.x) ** 2 + (y - ship.center.y) ** 2)

                    # Check if the distance is greater than the minimum safe distance
                    if distance_from_ship >= min_safe_distance:
                        break  # Position is safe, exit the loop and place the asteroid

                # Create the asteroid with the safe position
                asteroid_type = AsteroidType.LARGE  # Start with large asteroids
                velocity_x = random.uniform(-1, 1)
                velocity_y = random.uniform(-1, 1)
                asteroid = Asteroid(x, y, velocity_x, velocity_y, asteroid_type, screen_width, screen_height)
                self.asteroids.append(asteroid)

    def start_next_level(self, screen_width, screen_height, ship):
        """Start the next level by generating more asteroids."""
        self.level += 1  # Increase the level
        # Each level starts with 4 + (level-1) large asteroids
        asteroid_count = 1 + (self.level - 1)
        self.populate(asteroid_count, screen_width, screen_height, ship)

    def clear(self):
        """Clear all asteroids from the field."""
        self.asteroids = []
        #ship.bullets=[]

    def remove_destroyed_asteroids(self):
        """Remove asteroids that have been marked as destroyed."""
        self.asteroids = [
            asteroid for asteroid in self.asteroids if not asteroid.is_destroyed]

    def move_asteroids(self):
        """Move all asteroids in the field."""
        for asteroid in self.asteroids:
            asteroid.move()

    def check_ship_collision(self, ship):
        """Check if the ship collides with any asteroid."""
        for asteroid in self.asteroids:
            if asteroid.check_collision(ship):
                ship.ship_hit = True
                ship.destroy()  # Handle the ship's destruction
                ship.flash_screen()  # This should display the score

                # Regenerate the asteroid field
                self.regenerate_field(ship, self.asteroid_count)
                break  # Stop checking after the first collision

    def regenerate_field(self, ship, asteroid_count):
        """Clear the field and repopulate it with asteroids after a collision."""
        self.clear()  # Clear existing asteroids
        ship.center = Point(GRID_WIDTH // 2, GRID_HEIGHT // 2)  # Reset ship position (optional)
        self.populate(asteroid_count, GRID_WIDTH, GRID_HEIGHT, ship)  # Regenerate the field with new asteroids

    def check_bullet_collisions(self, ship, small_explosion_sound, medium_explosion_sound, large_explosion_sound):
        """Check if any bullets from the ship hit any asteroids."""
        bullets_to_remove = []
        new_asteroids = []  # To store newly split asteroids

        for bullet in ship.bullets:
            for asteroid in self.asteroids:
                if asteroid.is_destroyed:  # Skip already destroyed asteroids
                    continue

                if asteroid.check_collision(bullet):
                    print("Bullet hit asteroid!")
                    ship.hit_count += 1

                    bullet.is_destroyed = True  # Mark bullet as destroyed
                    bullets_to_remove.append(bullet)  # Mark bullet for removal

                    # Play appropriate explosion sound based on asteroid size
                    if asteroid.asteroid_type == AsteroidType.SMALL:
                        ship.score += 100
                        small_explosion_sound.play()

                    elif asteroid.asteroid_type == AsteroidType.MEDIUM:
                        ship.score += 50
                        medium_explosion_sound.play()
                    elif asteroid.asteroid_type == AsteroidType.LARGE:
                        ship.score += 20
                        large_explosion_sound.play()


                    # Split the asteroid only once
                    if not asteroid.is_destroyed:
                        asteroid.is_destroyed = True  # Mark asteroid as destroyed to prevent duplicate splits
                        new_asteroids.extend(asteroid.split())  # Split asteroid and add to new list

        # Remove collided bullets from the ship's bullet list
        ship.bullets = [bullet for bullet in ship.bullets if bullet not in bullets_to_remove]

        # Remove destroyed asteroids from the field
        self.remove_destroyed_asteroids()

        # Add the newly split asteroids to the field
        self.asteroids.extend(new_asteroids)



    def update_heartbeat(self):
        """Update the heartbeat sound based on the number of asteroids left."""
        remaining_asteroids = len(self.asteroids)

        if remaining_asteroids == 0:
            return  # No heartbeat when no asteroids are left

        # Adjust the interval based on how many asteroids are left
        self.heartbeat_interval = 0.5 + (remaining_asteroids / 10)

        current_time = time.time()
        if current_time - self.last_heartbeat_time >= self.heartbeat_interval:
            self.play_heartbeat()
            self.last_heartbeat_time = current_time

    def play_heartbeat(self):
        """Play the heartbeat sound using pygame."""
        self.heartbeat1_sound.play()  # You can alternate between sounds if desired

    def __repr__(self):
        return f"AsteroidField(asteroids={self.asteroids})"
