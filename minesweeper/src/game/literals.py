from typing import Literal, Union

# TODO: this file/filename feels clumsy


# TODO: constants in caps!
Result = Literal['victory', 'failure']

GameState = Union[Result, Literal['inProgress']]
"""
  - `inProgress` - game is in progress even when it's not started
  - `victory` - game is over - all mines have been correctly flagged
  - `failure` - uncovered tiles with a mine
"""
