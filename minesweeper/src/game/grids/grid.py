from abc import ABC, abstractmethod
from typing import List, Tuple

from src.common import Point
from src.game.tiles.tile import Tile


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

    def get_tile_at(self, x: int, y: int) -> Tile:
        return self[x, y]

    @abstractmethod
    def get_neighbours_of_tile_at(self, x: int, y: int) -> List[Tuple[Point, Tile]]:
        ...

    @abstractmethod
    def is_valid(self) -> bool:
        ...

    @abstractmethod
    def print(self) -> None:
        ...
