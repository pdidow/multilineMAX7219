import math
import random
from include.point import Point
from include.bullet import Bullet


class UFO:
    def __init__(self, ufo_type, screen_width, screen_height):
        """
        Initialize the UFO object
        :param ufo_type: 'large' or 'small'
        :param screen_width: width of the display
        :param screen_height: height of the display
        """
        self.type = ufo_type  # "large" or "small"
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = self.random_speed_based_on_type(self.type)
        # Direction: left-to-right or right-to-left
        self.direction = self.random_direction()
        self.position = self.set_starting_position(
            self.direction, screen_width, screen_height)
        self.bullet_speed = self.set_bullet_speed(self.type)
        self.is_alive = True
        self.fire_timer = self.random_fire_delay(self.type)
        self.animation_frame = 0  # To track current frame of UFO animation
        self.animation_speed = 5  # Change frame every 5 cycles
        self.animation_timer = 0  # Counter to control animation frame switching

        # Define four frames for the UFO animation
        self.frames = [
            [
                [0, 1, 1, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 1],
                [0, 1, 1, 0]
            ],
            [
                [0, 1, 1, 0],
                [1, 1, 1, 1],
                [0, 0, 1, 0],
                [0, 1, 1, 0]
            ],
            [
                [0, 1, 1, 0],
                [1, 1, 1, 1],
                [0, 1, 0, 0],
                [0, 1, 1, 0]
            ],
            [
                [0, 1, 1, 0],
                [1, 1, 1, 1],
                [1, 0, 0, 0],
                [0, 1, 1, 0]
            ]
        ]

        """Update UFO position and wrap around the screen."""
        if self.direction == "left_to_right":
            self.position.x += self.speed  # Move UFO to the right
        else:
            self.position.x -= self.speed  # Move UFO to the left

        # Screen wrapping logic
        if self.position.x < 0:
            self.position.x = self.screen_width
        elif self.position.x > self.screen_width:
            self.position.x = 0

        # Handle animation frame switching
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            # Cycle through frames
            self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_timer = 0

    def random_speed_based_on_type(self, ufo_type):
        """Set random speed based on UFO type."""
        if ufo_type == "large":
            return random.uniform(1, 2)  # Large UFO moves slower
        else:
            return random.uniform(2, 3.5)  # Small UFO moves faster

    def random_direction(self):
        """Set the UFO's movement direction (left to right or right to left)."""
        return random.choice(["left_to_right", "right_to_left"])

    def set_bullet_speed(self, ufo_type):
        """Set bullet speed based on UFO type."""
        if ufo_type == "large":
            return random.uniform(1, 2)
        else:
            return random.uniform(2, 3)

    def random_fire_delay(self, ufo_type):
        """Randomize fire delay based on UFO type."""
        if ufo_type == "large":
            return random.randint(80, 120)  # Large UFO fires less frequently
        else:
            return random.randint(40, 80)  # Small UFO fires more often

    def set_starting_position(self, direction, screen_width, screen_height):
        """Set the UFO's starting position based on its direction."""
        if direction == "left_to_right":
            start_x = 0  # Start at the left edge
        else:
            start_x = screen_width  # Start at the right edge

        # Print start_x to the console for debugging
        print(f"start_x: {start_x}")

        # Randomly position the UFO on the Y-axis
        # Adjust for UFO height (4 pixels)
        start_y = random.randint(0, screen_height - 4)

        # Return the starting position as a Point object (assuming Point is used in your game)

        return Point(start_x, start_y)

    def move(self):
        """Move the UFO across the screen and handle screen wrapping."""
        # Move UFO based on its direction
        if self.direction == "left_to_right":
            self.position.x += self.speed  # Move to the right
        else:
            self.position.x -= self.speed  # Move to the left

        # Screen wrapping logic: If UFO goes off one side, it reappears on the other
        if self.position.x < 0:
            self.position.x = self.screen_width  # Wrap around to the right
        elif self.position.x > self.screen_width:
            self.position.x = 0  # Wrap around to the left

    def fire_bullet(self, player_position):
        """Handle UFO shooting logic."""
        if self.fire_timer <= 0:
            if self.type == "large":
                # Large UFO fires randomly
                bullet_direction = self.random_direction()
            else:
                # Small UFO aims directly at the player
                bullet_direction = self.aim_at_player(player_position)

            # Calculate velocity based on the bullet direction
            bullet_velocity_x = bullet_direction.x * self.bullet_speed
            bullet_velocity_y = bullet_direction.y * self.bullet_speed

            # Define angle (you can calculate this based on direction if necessary)
            bullet_angle = math.atan2(bullet_direction.y, bullet_direction.x)

            # Define a lifespan for the bullet (e.g., how long it lives)
            bullet_lifespan = 100  # Adjust this based on your game�s needs

            # Create a bullet with direction and speed
            bullet = Bullet(self.position.x, self.position.y, bullet_velocity_x,
                            bullet_velocity_y, bullet_angle, bullet_lifespan)

            # Reset the fire timer
            self.fire_timer = self.random_fire_delay(self.type)

            return bullet  # Return the bullet to be added to the game
        else:
            # This needs to be aligned with the first 'if'
            self.fire_timer -= 1  # Countdown timer

    def check_collision(self, player_bullets):
        """Check if the UFO is hit by player bullets."""
        for bullet in player_bullets:
            # Create a Point object from bullet's x and y
            bullet_position = Point(bullet.x, bullet.y)

            # Check if the bullet collides with the UFO
            if self.collision_detected(bullet_position):
                self.is_alive = False
                return True  # UFO is destroyed
        return False

    def collision_detected(self, bullet_x, bullet_y):
        """Simple collision detection (bounding box)."""
        ufo_width, ufo_height = 4, 4  # Size of the UFO graphic (adjust if necessary)
        return (self.position.x <= bullet_x <= self.position.x + ufo_width and
                self.position.y <= bullet_y <= self.position.y + ufo_height)

    def draw(self, LEDMatrix):
        """Draw the UFO on the LED Matrix display using the current animation frame."""
        if self.is_alive:
            frame = self.frames[self.animation_frame]
            for y, row in enumerate(frame):
                for x, pixel in enumerate(row):
                    if pixel == 1:
                        LEDMatrix.gfx_set_px(
                            int(self.position.x + x),
                            int(self.position.y + y),
                            LEDMatrix.GFX_ON
                        )

    def set_starting_position(self, direction, screen_width, screen_height):
        """Set the UFO starting position based on its direction."""
        if direction == "left_to_right":
            start_x = 0  # Start from the left edge
        else:
            start_x = screen_width  # Start from the right edge
        start_y = random.randint(0, screen_height - 4)  # Random Y position
        return Point(start_x, start_y)

    def random_speed_based_on_type(self, ufo_type):
        """Set random speed based on UFO type."""
        if ufo_type == "large":
            return random.uniform(1, 2)  # Large UFO moves slower
        else:
            return random.uniform(2, 3.5)  # Small UFO moves faster

    def set_bullet_speed(self, ufo_type):
        """Set bullet speed based on UFO type."""
        if ufo_type == "large":
            return random.uniform(1, 2)
        else:
            return random.uniform(2, 3)

    def random_fire_delay(self, ufo_type):
        """Randomize fire delay based on UFO type."""
        if ufo_type == "large":
            return random.randint(80, 120)  # Large UFO fires less frequently
        else:
            return random.randint(40, 80)  # Small UFO fires more often

    def random_direction(self):
        """Set the UFO's movement direction (left to right or right to left)."""
        return random.choice(["left_to_right", "right_to_left"])

    def aim_at_player(self, player_position):
        """Aim directly at the player by calculating direction."""
        direction_x = player_position.x - self.position.x
        direction_y = player_position.y - self.position.y
        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
        # Normalize
        return Point(direction_x / magnitude, direction_y / magnitude)

    def collision_detected(self, bullet_position):
        """Simple collision detection (bounding box)."""
        ufo_width, ufo_height = 4, 4  # Size of the UFO graphic
        return (self.position.x <= bullet_position.x <= self.position.x + ufo_width and
                self.position.y <= bullet_position.y <= self.position.y + ufo_height)
