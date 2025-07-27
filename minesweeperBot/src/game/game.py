from typing import Literal, NamedTuple, Union

from src.game.board import Board


Result = Literal['victory', 'failure']

GameState = Union[Result, Literal['inProgress']]
"""
  - `inProgress` - game is in progress even when it's not started
  - `victory` - game is over - all mines have been correctly flagged
  - `failure` - uncovered tile with a mine
"""


class Game(NamedTuple):
    board: Board
    state: GameState
