from typing import override

from src.exceptions import FrozenInstanceError
from src.game.tiles import MineCount, Tile, Symbol


class FrozenTile(Tile):
    def __init__(self, tile: Tile) -> None:
        self._tile = tile

    @override
    def get_count(self) -> MineCount | None:
        return self._tile.get_count()

    @override
    def get_symbol(self) -> Symbol:
        return self._tile.get_symbol()

    @override
    def set_symbol(self, symbol: Symbol, mines: MineCount | None = None) -> None:
        raise FrozenInstanceError('This instance is frozen')
