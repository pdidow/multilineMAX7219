from enum import Enum

class AsteroidType(Enum):
    SMALL = (1, 2.5)  # size, speed multiplier
    MEDIUM = (2, 1.5)
    LARGE = (3, 1)

    @staticmethod
    def from_size(size):
        """Helper method to get the enum based on the size."""
        for asteroid_type in AsteroidType:  # Corrected reference to AsteroidType
            if asteroid_type.value[0] == size:
                return asteroid_type
        return None  # Return None if no matching size is found
