import time
import random
import pygame
from include.asteroid import Asteroid
from include.asteroidType import AsteroidType, get_random_asteroid_type

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

    def populate(self, count, screen_width, screen_height):
        """Populate the asteroid field with a number of random asteroids."""
        self.clear()  # Optional: clear existing asteroids before populating

        for _ in range(count):
            asteroid_type = AsteroidType.LARGE  # Always start with large asteroids
            x = random.uniform(0, screen_width)  # Random starting x position
            y = random.uniform(0, screen_height)  # Random starting y position
            velocity_x = random.uniform(-1, 1)  # Random x velocity
            velocity_y = random.uniform(-1, 1)  # Random y velocity

            # Ensure asteroids have some velocity (so no asteroid remains stationary)
            while velocity_x == 0 and velocity_y == 0:
                velocity_x = random.uniform(-1.5, 1.5)
                velocity_y = random.uniform(-1.5, 1.5)

            # Create the asteroid using the refactored Asteroid class
            asteroid = Asteroid(
                x=x,
                y=y,
                velocity_x=velocity_x,
                velocity_y=velocity_y,
                asteroid_type=asteroid_type,
                screen_width=screen_width,
                screen_height=screen_height
            )
            self.asteroids.append(asteroid)

    def start_next_level(self, screen_width, screen_height):
        """Start the next level by generating more asteroids."""
        self.level += 1  # Increase the level
        # Each level starts with 4 + (level-1) large asteroids
        asteroid_count = 4 + (self.level - 1)
        self.populate(asteroid_count, screen_width, screen_height)

    def clear(self):
        """Clear all asteroids from the field."""
        self.asteroids = []

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
                ship.destroy()  # Call the ship's destroy method or handle collision
                break  # Stop checking after the first collision

    def check_bullet_collisions(self, ship):
        """Check if any bullets from the ship hit any asteroids."""
        for bullet in ship.bullets:
            for asteroid in self.asteroids:
                if asteroid.check_collision(bullet):
                    print("Bullet hit asteroid!")
                    asteroid.is_destroyed = True  # Mark the asteroid as destroyed
                    bullet.is_destroyed = True  # Mark the bullet as destroyed
                    break  # Move to next bullet after first collision

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
