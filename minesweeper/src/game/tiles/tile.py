from abc import ABC, abstractmethod
from typing import Literal, assert_never, overload

from src.game.tiles import NonNumberSymbol, NumberSymbol, Symbol


class Tile(ABC):
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
    def set_symbol(self, symbol: NonNumberSymbol, mines: Literal[None]) -> None:
        ...

    @abstractmethod
    def set_symbol(self, symbol: Symbol, mines: int | None = None) -> None:
        ...

    def is_covered(self, include_question_marks: bool = True) -> bool:
        symbol = self.get_symbol()

        if symbol == 'COVERED' or symbol == 'FLAG':
            return True

        return symbol == 'QUESTION_MARK' and include_question_marks


def tile_to_char(tile: Tile) -> str:
    symbol = tile.get_symbol()

    match symbol:
        case 'COVERED':
            return 'O'
        case 'EXPLODED_MINE':
            return '*'
        case 'MINE':
            return '+'
        case 'WRONG_FLAG':
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
