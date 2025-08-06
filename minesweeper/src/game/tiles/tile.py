from abc import ABC, abstractmethod
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


COVERED_SYMBOLS = {'COVERED', 'FLAG', 'QUESTION_MARK'}


class Tile(ABC):
    @abstractmethod
    def get_count(self) -> int | None:
        ...

    @abstractmethod
    def set_count(self, count: int) -> None:
        ...

    @abstractmethod
    def get_symbol(self) -> Symbol:
        ...

    @abstractmethod
    def set_sign(self, sign: Sign) -> None:
        ...

    def is_covered(self) -> bool:
        return self.get_symbol() in COVERED_SYMBOLS
