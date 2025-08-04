from typing import Tuple, override

from src.game.grids.impl.shaped_grid import ShapedGrid
from src.game.tiles.tile import Tile


class MutableGrid(ShapedGrid):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    @override
    def __getitem__(self, key: Tuple[int, int]) -> Tile:
        x, y = key
        self._validate_position(x, y)
        return self._tiles[y][x]
