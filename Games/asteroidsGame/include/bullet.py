class Bullet:
    def __init__(self, x, y, velocity_x, velocity_y, angle, lifespan):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.angle = angle
        self.radius = 1
        self.lifespan = lifespan  # Time before the bullet expires

    def update_position(self):
        """Update the bullet's position based on its velocity."""
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifespan -= 1  # Decrease lifespan

    def get_position(self):
        """Return the current position of the bullet."""
        return self.x, self.y

    def __repr__(self):
        return (f"Bullet(x={self.x}, y={self.y}, "
                f"velocity_x={self.velocity_x}, velocity_y={self.velocity_y})")
