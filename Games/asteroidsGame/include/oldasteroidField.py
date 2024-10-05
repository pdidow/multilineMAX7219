import time
import random
import pygame
from include.asteroid import Asteroid
from include.asteroidType import AsteroidType # Importing the AsteroidTypes from the new file
# Initialize pygame's mixer for sound
pygame.mixer.init()

class AsteroidField:
    def __init__(self):
        self.asteroids = []  # An asteroidField is just a collection of asteroid objects
        self.heartbeat_interval = 2  # Start with a 2-second interval for the heartbeat sound
        self.last_heartbeat_time = time.time()  # Track the last time the heartbeat played

        # Load the heartbeat sounds using pygame
        self.heartbeat1_sound = pygame.mixer.Sound('sounds/beat1.wav')  # Replace with the path to your sound file
        self.heartbeat2_sound = pygame.mixer.Sound('sounds/beat2.wav')  # Replace with the path to your sound file

    def populate(self, count, screen_width, screen_height):
        types = [AsteroidType.SMALL, AsteroidType.MEDIUM, AsteroidType.LARGE]  # Use actual AsteroidType values
        self.clear()  # Optional: clear existing asteroids before populating
        for _ in range(count):
            size = random.choice([1, 2, 3])
            asteroid_type = random.choice(types)
            x = random.uniform(0, screen_width)  # Random starting x position
            y = random.uniform(0, screen_height)  # Random starting y position
            velocity_x = random.uniform(-1, 1)  # Random x velocity
            velocity_y = random.uniform(-1, 1)  # Random y velocity
            asteroid = Asteroid(x, y, velocity_x, velocity_y, asteroid_type, screen_width, screen_height)
            self.asteroids.append(asteroid)

    
    def clear(self):
        self.asteroids = []

    def remove_destroyed_asteroids(self):
        """Remove asteroids that have been destroyed."""
        #self.asteroids = [asteroid for asteroid in self.asteroids if not asteroid.is_destroyed()]
        self.asteroids = [asteroid for asteroid in self.asteroids if not asteroid.is_destroyed]


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
                    asteroid.destroy()  # Destroy the asteroid
                    bullet.destroy()  # Destroy the bullet
                    break  # Move to next bullet after first collision

    def update_heartbeat(self):
        """Update the heartbeat based on the number of asteroids left."""
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
        self.heartbeat1_sound.play()  # Assuming you want to play heartbeat1_sound; adjust if needed

    def __repr__(self):
        return f"AsteroidField(asteroids={self.asteroids})"
