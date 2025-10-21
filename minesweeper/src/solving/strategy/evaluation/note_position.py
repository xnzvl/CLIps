from enum import Enum, auto, unique


@unique
class NotePosition(Enum):
    NONE                 = auto()
    AFTER_PER_DIFFICULTY = auto()
    AT_THE_END           = auto()
