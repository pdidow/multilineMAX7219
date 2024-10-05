from enum import Enum, auto
from typing import List, Dict
import random

class AsteroidType(Enum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()

    def get_speed_multiplier(self) -> float:
        return self._data["speed_multiplier"]

    def get_graphic(self) -> List[List[int]]:
        return self._data["graphic"]

    @property
    def _data(self) -> Dict[str, float or List[List[int]]]:
        data = {
            AsteroidType.SMALL: {"speed_multiplier": 2.5, "graphic": [
                [0, 1, 1, 0],
                [0, 1, 1, 0]
            ]},
            AsteroidType.MEDIUM: {"speed_multiplier": 1.5, "graphic": [
                [0, 1, 1, 1],
                [1, 0, 1, 1],
                [1, 1, 1, 1]
            ]},
            AsteroidType.LARGE: {"speed_multiplier": 1.0, "graphic": [
                [1, 1, 1, 0],
                [0, 1, 1, 0],
                [1, 1, 1, 1],
                [1, 1, 1, 0]
            ]}
        }
        return data[self]

def get_random_asteroid_type() -> AsteroidType:
    return random.choice(list(AsteroidType))
