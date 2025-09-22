from src.common import Move, Action, Point


class Input:
    def __init__(self, action: Action, point: Point | None = None) -> None:
        if action == Action.RESET or action == Action.QUIT:
            assert point is None  # TODO: some message to asserts would be nice
            self.move = None

        else:
            assert point is not None
            self.move = Move(action, point)

        self.action = action
