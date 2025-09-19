from abc import ABC, abstractmethod
from typing import List, Self, Tuple

from src.common import Point
from src.game.tiles import Symbol, Tile


class GridIterator[T: Tile](ABC):
    def __iter__(self) -> Self:
        return self

    @abstractmethod
    def __next__(self) -> Tuple[Point, T]:
        ...

    def to_list(self) -> List[Tuple[Point, T]]:
        return [t for t in self]


class Grid[T: Tile](ABC):
    @abstractmethod
    def __getitem__(self, key: Tuple[int, int] | Point) -> T:
        ...

    @abstractmethod
    def __iter__(self) -> GridIterator[T]:
        ...

    @abstractmethod
    def get_width(self) -> int:
        ...

    @abstractmethod
    def get_height(self) -> int:
        ...

    @abstractmethod
    def neighbourhood_of(self, x: int, y: int) -> GridIterator[T]:
        ...

    # TODO: update class usage
    @abstractmethod
    def neighbourhood_with_symbol_of(self, x: int, y: int, *desired_symbols: Symbol) -> GridIterator[T]:
        ...

    @abstractmethod
    def wide_neighbourhood_of(self, x: int, y: int) -> GridIterator[T]:
        ...

    @abstractmethod
    def wide_neighbourhood_with_symbol_of(self, x: int, y: int, *desired_symbols: Symbol) -> GridIterator[T]:
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
