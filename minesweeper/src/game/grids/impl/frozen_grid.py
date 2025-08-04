from typing import List, Tuple, override

from src.common import Point
from src.game.grids.grid import Grid, GridIterator
from src.game.tiles.impl.frozen_tile import FrozenTile
from src.game.tiles.tile import Tile


class FrozenGridIterator(GridIterator):
    def __init__(self, iterator: GridIterator) -> None:
        self._iterator = iterator

    @override
    def __next__(self) -> Tuple[Point, Tile]:
        p, t = next(self._iterator)
        return p, FrozenTile(t)


class FrozenGrid(Grid):
    def __init__(self, grid: Grid) -> None:
        self._grid = grid

    def __getitem__(self, key: Tuple[int, int]) -> Tile:
        # TODO: use *key instead? is it a more python-ish way?
        x, y = key
        return self._grid[x, y]

    def __iter__(self) -> GridIterator:
        return FrozenGridIterator(iter(self._grid))

    def get_width(self) -> int:
        return self._grid.get_width()

    def get_height(self) -> int:
        return self._grid.get_height()

    def get_neighbours_of_tile_at(self, x: int, y: int) -> List[Tuple[Point, Tile]]:
        return [(p, FrozenTile(t)) for p, t in self._grid.get_neighbours_of_tile_at(x, y)]

    def is_valid(self) -> bool:
        return self._grid.is_valid()

    def print(self) -> None:
        return self._grid.print()
