from typing import NamedTuple, Literal


MouseButton = Literal['primary', 'secondary', 'middle']


class Point(NamedTuple):
    x: int
    y: int


class Dimensions(NamedTuple):
    width: int
    height: int


class Configuration(NamedTuple):
    offsets: Point
    dimensions: Dimensions


class Move(NamedTuple):
    button: MouseButton
    tile: Point
