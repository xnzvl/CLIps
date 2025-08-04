from abc import ABC, abstractmethod

from src.game.tiles import Sign, Symbol


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

    @abstractmethod
    def is_covered(self) -> bool:
        ...
