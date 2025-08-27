from typing import Literal, NamedTuple

from src.common import Move


InputType = Literal['MOVE', 'RESET', 'QUIT']


class Input(NamedTuple):
    type: InputType
    move: Move | None = None
