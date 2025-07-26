from typing import NamedTuple, Literal, Union

from src.game.board import Board


Result = Literal['victory', 'failure']

GameState = Union[Result, Literal['inProgress']]
"""
  - `inProgress` - game is in progress even when it's not started
  - `victory` - game is over - all mines have been correctly flagged
  - `failure` - uncovered tile with a mine
"""

MouseButton = Literal['left', 'middle', 'right']


class Game(NamedTuple):
    board: Board
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
