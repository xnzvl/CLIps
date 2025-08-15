from typing import NamedTuple, Literal


MouseButton = Literal['primary', 'secondary', 'middle']
# TODO: documentation


class Point(NamedTuple):
    x: int
    y: int


class Dimensions(NamedTuple):
    width: int
    height: int


class Configuration(NamedTuple):
    offsets: Point
    dimensions: Dimensions


# TODO: change!
#       instead of button I want to be able to choose to which Symbol the tile will be turned into
class Move(NamedTuple):
    button: MouseButton
    tile: Point
