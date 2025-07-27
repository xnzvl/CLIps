from typing import Literal, Union


Sign = Literal[
    'COVERED',
    'FLAG',
    'QUESTION_MARK',
    'EXPLODED_MINE',
    'MINE',
    'BAD_MINE',
    'EMPTY'
]

Symbol = Union[Sign, Literal['NUMBER']]


class Tile:
    def __init__(self) -> None:
        self._symbol: Symbol = 'COVERED'
        self._count: int | None = None

    def get_count(self) -> int | None:
        return self._count

    def set_count(self, count: int) -> None:
        if count < 0:
            raise ValueError(f"number of mines in the proximity cannot be lower than 0 (received {count})")
        if count > 8:
            raise ValueError(f"number of mines in the proximity cannot be greater than 8 (received {count})")

        if count == 0:
            self._symbol = 'EMPTY'
            self._count = None
        else:
            self._symbol = 'NUMBER'
            self._count = count

    def get_symbol(self) -> Symbol:
        return self._symbol

    def set_sign(self, sign: Sign) -> None:
        self._symbol = sign
        self._count = None
