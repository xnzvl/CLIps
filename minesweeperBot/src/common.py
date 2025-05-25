from typing import NamedTuple, List, Literal, Set, Union


TileObservation = Literal['O', '1', '2', '3', '4', '5', '6', '7', '8', ' ', 'F', '*', '+']
"""
  - `O` covered tile
  - number presents count of mines in proximity
  - `*space*` for an empty tile
  - `F` flag
  - `*` exploded mine
  - `+` mine
"""

Result = Literal['victory', 'failure']

GameState = Union[Result, Literal['inProgress']]
"""
  - `inProgress` - game is in progress even when it's not started
  - `victory` - game is over - all mines have been correctly flagged
  - `failure` - uncovered tile with a mine
"""

BoardObservation = List[List[TileObservation]]

MouseButton = Literal['left', 'middle', 'right']


class GameObservation(NamedTuple):
    board: BoardObservation
    state: GameState


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


NUMBER_TILE_OBSERVATION: Set[TileObservation] = {'1', '2', '3', '4', '5', '6', '7', '8'}
