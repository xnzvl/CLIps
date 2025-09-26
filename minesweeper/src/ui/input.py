from typing import Literal, overload

from src.common import Action, Move, Point


ActionWithPoint = Literal[
    Action.UNCOVER,
    Action.FLAG,
    Action.QUESTION_MARK,
    Action.CLEAR
]
ActionWithoutPoint = Literal[
    Action.RESET,
    Action.QUIT
]


class Input:
    @overload
    def __init__(self, action: ActionWithPoint, point: Point):
        ...

    @overload
    def __init__(self, action: ActionWithoutPoint, point: Literal[None] = None):
        ...

    def __init__(self, action: Action, point: Point | None = None) -> None:
        if action == Action.RESET or action == Action.QUIT:
            assert point is None
            self.move = None
        else:
            assert point is not None
            self.move = Move(action, point)

        self.action = action
