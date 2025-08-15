from abc import ABC, abstractmethod
from typing import List, Tuple

from src.common import Point
from src.game.tiles.tile import Symbol, Tile


class GridIterator(ABC):
    @abstractmethod
    def __next__(self) -> Tuple[Point, Tile]:
        ...


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
    def get_neighbours_of_tile_at(self, x: int, y: int) -> List[Tuple[Point, Tile]]:
        ...

    @abstractmethod
    def is_valid(self) -> bool:
        ...

    @abstractmethod
    def print(self) -> None:
        ...

    def get_tile_at(self, x: int, y: int) -> Tile:
        return self[x, y]

    # TODO: update class usage
    def count_symbol_in_neighbourhood(self, x: int, y: int, symbol: Symbol) -> int:
        return len(
            [
                None
                for _, neighbour in self.get_neighbours_of_tile_at(x, y)
                if neighbour.get_symbol() == symbol
            ]
        )

    # TODO: update class usage
    def get_neighbours_with_symbol(self, x: int, y: int, *desired_symbols: Symbol) -> List[Tuple[Point, Tile]]:
        white_list = set(desired_symbols)
        return [
            (p, t)
            for p, t in self.get_neighbours_of_tile_at(x, y)
            if t.get_symbol() in white_list
        ]
