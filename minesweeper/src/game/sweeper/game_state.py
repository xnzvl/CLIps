from enum import Enum
from typing import Literal


class GameState(Enum):
    """
      - `IN_PROGRESS` - game is in progress even when it's not started
      - `VICTORY` - game is over - all non-mines are revealed
      - `FAILURE` - game is over - uncovered tiles with a mine
    """
    VICTORY     = 'VICTORY'
    FAILURE     = 'FAILURE'
    IN_PROGRESS = 'IN_PROGRESS'


Result = Literal[GameState.VICTORY, GameState.FAILURE]
