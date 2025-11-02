from abc import ABC, abstractmethod
from typing import Literal, assert_never, cast, overload

from src.game.tiles import Symbol


type NumberSymbol = Literal[
    Symbol.NUMBER
]
type NonNumberSymbol = Literal[
    Symbol.MINE,
    Symbol.EMPTY,
    Symbol.COVER,
    Symbol.FLAG,
    Symbol.QUESTION_MARK,
    Symbol.EXPLODED_MINE,
    Symbol.WRONG_FLAG
]

type MineCount = Literal[1, 2, 3, 4, 5, 6, 7, 8]
type TileChar = Literal[
    'O', '*', '+', 'X', 'F', '?', ' ',
    '1', '2', '3', '4', '5', '6', '7', '8'
]


class Tile(ABC):
    def __str__(self) -> str:
        return f'{type(self).__name__}(symbol={self.get_symbol()})'

    @abstractmethod
    def get_count(self) -> MineCount | None:
        ...

    @abstractmethod
    def get_symbol(self) -> Symbol:
        ...

    @overload
    def set_symbol(self, symbol: NumberSymbol, mines: MineCount) -> None:
        ...

    @overload
    def set_symbol(self, symbol: NonNumberSymbol, mines: Literal[None] = None) -> None:
        ...

    @abstractmethod
    def set_symbol(self, symbol: Symbol, mines: MineCount | None = None) -> None:
        ...

    def is_covered(self, include_question_marks: bool = True) -> bool:
        symbol = self.get_symbol()
        return symbol == Symbol.COVER or (include_question_marks and symbol == Symbol.QUESTION_MARK)


def tile_to_char(tile: Tile) -> TileChar:
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
            return cast(TileChar, str(tile.get_count()))
        case Symbol.EMPTY:
            return ' '
        case _:
            assert_never(symbol)
