from abc import ABC, abstractmethod
from typing import Literal, assert_never


Sign = Literal[
    'COVERED',
    'FLAG',
    'QUESTION_MARK',
    'EXPLODED_MINE',
    'MINE',
    'BAD_MINE',
    'EMPTY'
]

Symbol = Literal[Sign, Literal['NUMBER']]


class Tile(ABC):
    def __str__(self) -> str:
        return f'{type(self).__name__}({tile_to_char(self)})'

    @abstractmethod
    def get_count(self) -> int | None:
        ...

    @abstractmethod
    def set_count(self, count: int) -> None:
        ...

    @abstractmethod
    def get_symbol(self) -> Symbol:
        ...

    @abstractmethod
    def set_sign(self, sign: Sign) -> None:
        ...

    def is_covered(self) -> bool:
        match self.get_symbol():
            case 'COVERED' | 'FLAG' | 'QUESTION_MARK':
                return True
        return False


def tile_to_char(tile: Tile) -> str:
    symbol = tile.get_symbol()

    match symbol:
        case 'COVERED':
            return 'O'
        case 'EXPLODED_MINE':
            return '*'
        case 'MINE':
            return '+'
        case 'BAD_MINE':
            return 'X'
        case 'FLAG':
            return 'F'
        case 'QUESTION_MARK':
            return '?'
        case 'NUMBER':
            return str(tile.get_count())
        case 'EMPTY':
            return ' '
        case _:
            assert_never(symbol)
