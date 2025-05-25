class Tile:
    def __init__(self) -> None:
        self._count = 0
        self._isFlag = False
        self._isMine = False
        self._isCovered = False
        self.set_covered()

    def get_count(self) -> int:
        return self._count

    def set_count(self, count: int) -> None:
        if count < 0:
            raise ValueError(f"number of mines in the proximity cannot be lower than 0 (received {count})")
        if count > 8:
            raise ValueError(f"number of mines in the proximity cannot be greater than 8 (received {count})")

        self._count = count
        self._isFlag = False
        self._isMine = False
        self._isCovered = False

    def is_covered(self) -> bool:
        return self._isCovered

    def set_covered(self) -> None:
        self._count = 0
        self._isFlag = False
        self._isMine = False
        self._isCovered = True

    def is_flag(self) -> bool:
        return self._isFlag

    def place_flag(self) -> None:
        self._count = 0
        self._isFlag = True
        self._isMine = False
        self._isCovered = True

    def is_mine(self) -> bool:
        return self._isMine

    def place_mine(self, uncover: bool) -> None:
        self._count = 0
        self._isFlag = False
        self._isMine = True
        self._isCovered = not uncover

    def set_empty(self) -> None:
        self._count = 0
        self._isFlag = False
        self._isMine = False
        self._isCovered = False
