from typing import Literal

from src.common import Move, Action, Point


InputType = Literal[Action, 'RESET', 'QUIT']


class Input:
    def __init__(self, input_type: InputType, point: Point | None = None) -> None:
        if input_type == 'RESET' or input_type == 'QUIT':
            assert point is None  # TODO: some message to asserts would be nice
            self.move = None

        else:
            assert point is not None
            self.move = Move(input_type, point)

        self.type = input_type
