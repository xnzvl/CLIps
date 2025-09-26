from typing import Literal, overload

from src.common import Action, Move, MoveAction, MovelessAction, Point


class Input:
    @overload
    def __init__(self, action: MoveAction, point: Point):
        ...

    @overload
    def __init__(self, action: MovelessAction, point: Literal[None] = None):
        ...

    def __init__(self, action: Action, point: Point | None = None) -> None:
        if action == Action.RESET or action == Action.QUIT:
            assert point is None
            self.move = None
        else:
            assert point is not None
            self.move = Move(action, point)

        self.action = action
