from abc import ABC, abstractmethod

from src.common import Configuration, Move


class Clicker(ABC):
    def __init__(self, configuration: Configuration) -> None:
        self._offsets = configuration.offsets
        self._dimensions = configuration.dimensions

    @abstractmethod
    def do(self, move: Move) -> None:
        ...

    @abstractmethod
    def reset(self) -> None:
        ...
