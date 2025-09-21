from typing import override

from src.game.tiles import Symbol, Tile


class MutableTile(Tile):
    def __init__(self) -> None:
        self._symbol: Symbol = 'COVERED'
        self._mine_count: int | None = None

    @staticmethod
    def _check_mine_count(count: int) -> None:
        if count < 0:
            raise ValueError(f"number of mines in the proximity cannot be lower than 0 (received {count})")
        if count > 8:
            raise ValueError(f"number of mines in the proximity cannot be greater than 8 (received {count})")

    @override
    def get_count(self) -> int | None:
        return self._mine_count

    @override
    def get_symbol(self) -> Symbol:
        return self._symbol

    @override
    def set_symbol(self, symbol: Symbol, mines: int | None = None) -> None:
        if symbol == 'NUMBER':
            assert mines is not None
            self._check_mine_count(mines)

        self._symbol = symbol
        self._mine_count = mines
