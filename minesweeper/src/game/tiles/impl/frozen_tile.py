from typing import override

from src.exceptions import FrozenInstanceError
from src.game.tiles import Sign, Symbol
from src.game.tiles.tile import Tile


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
