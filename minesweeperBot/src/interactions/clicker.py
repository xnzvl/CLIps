from abc import ABC, abstractmethod

from src.common import Configuration, Move


class Clicker(ABC):
    def __init__(self, configuration: Configuration) -> None:
        self._offsets = configuration.offsets
        self._dimensions = configuration.dimensions
        self._tile_size = configuration.tile_size

    @abstractmethod
    def do(self, move: Move) -> None:
        ...
