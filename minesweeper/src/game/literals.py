from typing import Literal, Union

# TODO: this file/filename feels clumsy


Result = Literal['VICTORY', 'FAILURE']

GameState = Union[Result, Literal['IN_PROGRESS']]
"""
  - `IN_PROGRESS` - game is in progress even when it's not started
  - `VICTORY` - game is over - all mines have been correctly flagged
  - `FAILURE` - uncovered tiles with a mine
"""
