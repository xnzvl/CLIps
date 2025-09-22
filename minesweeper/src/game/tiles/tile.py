from abc import ABC, abstractmethod
from typing import Literal, assert_never, overload

from src.game.tiles import Symbol


NumberSymbol = Literal[
    Symbol.NUMBER
]
NonNumberSymbol = Literal[
    Symbol.MINE,
    Symbol.EMPTY,
    Symbol.COVER,
    Symbol.FLAG,
    Symbol.QUESTION_MARK,
    Symbol.EXPLODED_MINE,
    Symbol.WRONG_FLAG
]


class Tile(ABC):
    @staticmethod
    def _check_mine_count(count: int) -> None:
        if count < 0:
            raise ValueError(f"number of mines in the proximity cannot be lower than 0 (received {count})")
        if count > 8:
            raise ValueError(f"number of mines in the proximity cannot be greater than 8 (received {count})")

    def __str__(self) -> str:
        return f'{type(self).__name__}({tile_to_char(self)})'

    @abstractmethod
    def get_count(self) -> int | None:
        ...

    @abstractmethod
    def get_symbol(self) -> Symbol:
        ...

    @overload
    def set_symbol(self, symbol: NumberSymbol, mines: int) -> None:
        ...

    @overload
    def set_symbol(self, symbol: NonNumberSymbol, mines: Literal[None] = None) -> None:
        ...

    @abstractmethod
    def set_symbol(self, symbol: Symbol, mines: int | None = None) -> None:
        ...

    def is_covered(self, include_question_marks: bool = True) -> bool:
        symbol = self.get_symbol()

        if symbol == Symbol.COVER or symbol == Symbol.FLAG:
            return True

        return symbol == Symbol.QUESTION_MARK and include_question_marks


def tile_to_char(tile: Tile) -> str:
    symbol = tile.get_symbol()

    match symbol:
        case Symbol.COVER:
            return 'O'
        case Symbol.EXPLODED_MINE:
            return '*'
        case Symbol.MINE:
            return '+'
        case Symbol.WRONG_FLAG:
            return 'X'
        case Symbol.FLAG:
            return 'F'
        case Symbol.QUESTION_MARK:
            return '?'
        case Symbol.NUMBER:
            return str(tile.get_count())
        case Symbol.EMPTY:
            return ' '
        case _:
            assert_never(symbol)
