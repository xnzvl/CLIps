from abc import ABC, abstractmethod
from typing import Literal, Set, assert_never, override

from src.exceptions import FrozenInstanceError


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


COVERED_SYMBOLS: Set[Symbol] = {'COVERED', 'FLAG', 'QUESTION_MARK'}


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
        return self.get_symbol() in COVERED_SYMBOLS


class MutableTile(Tile):
    def __init__(self) -> None:
        self._symbol: Symbol = 'COVERED'
        self._count: int | None = None

    @override
    def get_count(self) -> int | None:
        return self._count

    @override
    def set_count(self, count: int) -> None:
        if count < 0:
            raise ValueError(f"number of mines in the proximity cannot be lower than 0 (received {count})")
        if count > 8:
            raise ValueError(f"number of mines in the proximity cannot be greater than 8 (received {count})")

        if count == 0:
            self._symbol = 'EMPTY'
            self._count = None
        else:
            self._symbol = 'NUMBER'
            self._count = count

    @override
    def get_symbol(self) -> Symbol:
        return self._symbol

    @override
    def set_sign(self, sign: Sign) -> None:
        self._symbol = sign
        self._count = None


class TranspaTile(MutableTile, ABC):
    def __init__(self) -> None:
        super().__init__()
        self._is_transparent = True

    @override
    def get_count(self) -> int | None:
        return None if self._is_transparent else super().get_count()

    @override
    def get_symbol(self) -> Symbol:
        return 'COVERED' if self._is_transparent else super().get_symbol()

    def set_transparency(self, transparency: bool) -> None:
        self._is_transparent = transparency


class FrozenTile(Tile):
    def __init__(self, tile: Tile) -> None:
        self._tile = tile

    @override
    def get_count(self) -> int | None:
        return self._tile.get_count()

    @override
    def set_count(self, count: int) -> None:
        raise FrozenInstanceError('cannot set mine count of frozen tiles')

    @override
    def get_symbol(self) -> Symbol:
        return self._tile.get_symbol()

    @override
    def set_sign(self, sign: Sign) -> None:
        raise FrozenInstanceError('cannot set tiles sign of frozen tiles')

    @override
    def is_covered(self) -> bool:
        return self._tile.is_covered()


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
