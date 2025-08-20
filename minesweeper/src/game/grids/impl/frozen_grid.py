from typing import Tuple, override

from src.common import Point
from src.game.grids.grid import Grid, GridIterator
from src.game.tiles.impl.frozen_tile import FrozenTile
from src.game.tiles.tile import Tile, Symbol


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

    @override
    def __getitem__(self, key: Tuple[int, int]) -> Tile:
        return self._grid[*key]

    @override
    def __iter__(self) -> GridIterator:
        return FrozenGridIterator(iter(self._grid))

    @override
    def get_width(self) -> int:
        return self._grid.get_width()

    @override
    def get_height(self) -> int:
        return self._grid.get_height()

    @override
    def neighbourhood_of(self, x: int, y: int) -> GridIterator:
        return FrozenGridIterator(self._grid.neighbourhood_of(x, y))

    @override
    def neighbourhood_with_symbol_of(self, x: int, y: int, *desired_symbols: Symbol) -> GridIterator:
        return FrozenGridIterator(self._grid.neighbourhood_with_symbol_of(x, y, *desired_symbols))

    @override
    def wide_neighbourhood_of(self, x: int, y: int) -> GridIterator:
        return FrozenGridIterator(self._grid.wide_neighbourhood_of(x, y))

    @override
    def wide_neighbourhood_with_symbol_of(self, x: int, y: int, *desired_symbols: Symbol) -> GridIterator:
        return FrozenGridIterator(self._grid.wide_neighbourhood_with_symbol_of(x, y, *desired_symbols))

    @override
    def is_valid(self) -> bool:
        return self._grid.is_valid()

    @override
    def print(self) -> None:
        return self._grid.print()
