from enum import Enum, auto
from typing import List, Dict
from dataclasses import dataclass
import random


class AsteroidType(Enum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()

    @classmethod
    def data(cls) -> Dict['AsteroidType', Dict[str, float or List[List[int]]]]:
        """Class-level dictionary storing asteroid type data."""
        return {
            cls.SMALL: {
                "speed_multiplier": 2.5,
                "graphic": [
                    [0, 1, 1, 0],
                    [0, 1, 1, 0]
                ]
            },
            cls.MEDIUM: {
                "speed_multiplier": 1.5,
                "graphic": [
                    [0, 1, 1, 0],
                    [1, 0, 0, 1],
                    [0, 1, 1, 0]
                ]
            },
            cls.LARGE: {
                "speed_multiplier": 1.0,
                "graphic": [
                    [0, 1, 1, 0],
                    [1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [0, 1, 1, 0]
                ]
            }
        }

    def get_speed_multiplier(self) -> float:
        return self.data()[self]["speed_multiplier"]

    def get_graphic(self) -> List[List[int]]:
        return self.data()[self]["graphic"]


def get_random_asteroid_type() -> AsteroidType:
    """Get a random asteroid type (small, medium, or large)."""
    return random.choice(list(AsteroidType))
