from typing import NamedTuple, Literal


Action = Literal['UNCOVER', 'FLAG', 'PLACE_QUESTION_MARK', 'CLEAR']


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
    action: Action
    tile: Point
