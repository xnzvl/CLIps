from enum import Enum, auto, unique


@unique
class Symbol(Enum):
    COVERED = auto()
    FLAG = auto()
    QUESTION_MARK = auto()
    EXPLODED_MINE = auto()
    MINE = auto()
    BAD_MINE = auto()
    NUMBER = auto()
    EMPTY = auto()
