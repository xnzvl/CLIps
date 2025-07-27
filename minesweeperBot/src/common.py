from typing import NamedTuple, Literal


MouseButton = Literal['left', 'middle', 'right']


class Point(NamedTuple):
    x: int
    y: int


class Dimensions(NamedTuple):
    width: int
    height: int


class Configuration(NamedTuple):
    offsets: Point
    dimensions: Dimensions
    tile_size: int


class Move(NamedTuple):
    button: MouseButton
    tile: Point
