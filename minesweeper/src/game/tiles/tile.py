from abc import ABC, abstractmethod
from typing import Literal, Union, assert_never

Sign = Literal[
    'COVERED',
    'FLAG',
    'QUESTION_MARK',
    'EXPLODED_MINE',
    'MINE',
    'BAD_MINE',
    'EMPTY'
]

Symbol = Union[Sign, Literal['NUMBER']]


COVERED_SYMBOLS = {'COVERED', 'FLAG', 'QUESTION_MARK'}


class Tile(ABC):
    def __str__(self) -> str:
        return f'{type(self).__name__}({tile_to_str(self)})'

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
        return self.get_symbol() in COVERED_SYMBOLS


def tile_to_str(tile: Tile) -> str:
    match tile.get_symbol():
        case 'COVERED':
            the_string = 'O'
        case 'EXPLODED_MINE':
            the_string = '*'
        case 'MINE':
            the_string = '+'
        case 'BAD_MINE':
            the_string = 'X'
        case 'FLAG':
            the_string = 'F'
        case 'QUESTION_MARK':
            the_string = '?'
        case 'NUMBER':
            the_string = tile.get_count()
        case 'EMPTY':
            the_string = ' '
        case _:
            assert_never(tile.get_symbol())

    return the_string
