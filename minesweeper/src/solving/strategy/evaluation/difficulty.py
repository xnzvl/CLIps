from enum import Enum, unique


@unique
class Difficulty(Enum):
    # difficulty | mine coefficient
    EASY         = (0, 8.1)
    INTERMEDIATE = (1, 6.4)
    HARD         = (2, 4.8)
