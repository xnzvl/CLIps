from typing import List

from src.common import Dimensions
from src.game.grids import Grid
from src.game.tiles import TileChars, Tile, tile_to_char


def shape_to_dimensions(shape: List[str]) -> Dimensions:
    height = len(shape)
    if height == 0:
        raise ValueError('shape must not be empty')

    width = len(shape[0])
    if width == 0:
        raise ValueError('shape row must not be empty')

    for row in shape:
        if len(row) != width:
            raise ValueError('each shape row must have the same length')

        for char in row:
            if char not in TileChars:
                raise ValueError(f'character {char} is not a TileChar')

    return Dimensions(
        width=width,
        height=height
    )


def compare_grid_with_shape[T: Tile](grid: Grid[T], shape: List[str]) -> bool:
    shape_dimensions = shape_to_dimensions(shape)

    if grid.get_dimensions() != shape_dimensions:
        return False

    for p, t in grid:
        if shape[p.y][p.x] != tile_to_char(t):
            return False

    return True
