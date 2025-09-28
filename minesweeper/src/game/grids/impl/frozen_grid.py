from typing import Tuple, override

from src.common import Point, Dimensions
from src.game.grids import GridIterator, Grid
from src.game.tiles import Tile, FrozenTile, Symbol


class FrozenGridIterator(GridIterator[Tile]):
    def __init__[T: Tile](self, iterator: GridIterator[T]) -> None:
        self._iterator = iterator

    @override
    def __next__(self) -> Tuple[Point, Tile]:
        p, t = next(self._iterator)
        return p, FrozenTile(t)


class FrozenGrid(Grid[Tile]):
    def __init__[T: Tile](self, grid: Grid[T]) -> None:
        self._grid = grid

    @override
    def __getitem__(self, key: Tuple[int, int] | Point) -> Tile:
        return self._grid[key]

    @override
    def __iter__(self) -> GridIterator[Tile]:
        return FrozenGridIterator(iter(self._grid))

    @override
    def get_dimensions(self) -> Dimensions:
        return self._grid.get_dimensions()

    @override
    def neighbourhood_of(self, x: int, y: int) -> GridIterator[Tile]:
        return FrozenGridIterator(self._grid.neighbourhood_of(x, y))

    @override
    def neighbourhood_with_symbol_of(self, x: int, y: int, *desired_symbols: Symbol) -> GridIterator[Tile]:
        return FrozenGridIterator(self._grid.neighbourhood_with_symbol_of(x, y, *desired_symbols))

    @override
    def wide_neighbourhood_of(self, x: int, y: int) -> GridIterator[Tile]:
        return FrozenGridIterator(self._grid.wide_neighbourhood_of(x, y))

    @override
    def wide_neighbourhood_with_symbol_of(self, x: int, y: int, *desired_symbols: Symbol) -> GridIterator[Tile]:
        return FrozenGridIterator(self._grid.wide_neighbourhood_with_symbol_of(x, y, *desired_symbols))

    @override
    def is_valid(self) -> bool:
        return self._grid.is_valid()

    @override
    def print(self) -> None:
        return self._grid.print()
