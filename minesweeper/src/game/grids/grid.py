from abc import ABC, abstractmethod
from typing import List, Self, Tuple

from src.common import Point
from src.game.tiles.tile import Symbol, Tile


class GridIterator(ABC):
    def __iter__(self) -> Self:
        return self

    @abstractmethod
    def __next__(self) -> Tuple[Point, Tile]:
        ...

    def to_list(self) -> List[Tuple[Point, Tile]]:
        return [t for t in self]

class Grid(ABC):
    @abstractmethod
    def __getitem__(self, key: Tuple[int, int]) -> Tile:
        ...

    @abstractmethod
    def __iter__(self) -> GridIterator:
        ...

    @abstractmethod
    def get_width(self) -> int:
        ...

    @abstractmethod
    def get_height(self) -> int:
        ...

    @abstractmethod
    def neighbourhood_of(self, x: int, y: int) -> GridIterator:
        ...

    # TODO: update class usage
    @abstractmethod
    def neighbourhood_with_symbol_of(self, x: int, y: int, *desired_symbols: Symbol) -> GridIterator:
        ...

    @abstractmethod
    def wide_neighbourhood_of(self, x: int, y: int) -> GridIterator:
        ...

    @abstractmethod
    def wide_neighbourhood_with_symbol_of(self, x: int, y: int, *desired_symbols: Symbol) -> GridIterator:
        ...

    @abstractmethod
    def is_valid(self) -> bool:
        ...

    @abstractmethod
    def print(self) -> None:
        ...

    # TODO: update class usage
    def count_symbol_in_neighbourhood(self, x: int, y: int, symbol: Symbol) -> int:
        return len(
            [
                None
                for _, t in self.neighbourhood_of(x, y)
                if t.get_symbol() == symbol
            ]
        )
