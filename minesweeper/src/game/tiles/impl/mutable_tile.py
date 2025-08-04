from typing import override

from src.game.tiles import Sign, Symbol, COVERED_SYMBOLS
from src.game.tiles.tile import Tile


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

    @override
    def is_covered(self) -> bool:
        return self._symbol in COVERED_SYMBOLS
