from abc import ABC, abstractmethod

from src.common import BoardObservation, Configuration, Dimensions, GameObservation, GameState, Point


class Observer(ABC):
    def __init__(self, configuration: Configuration) -> None:
        self._offsets = configuration.offsets
        self._dimensions = configuration.dimensions
        self._tile_size = configuration.tile_size

    def get_offsets(self) -> Point:
        return self._offsets

    def get_dimensions(self) -> Dimensions:
        return self._dimensions

    def get_tile_size(self) -> int:
        return self._tile_size

    def observe_game(self) -> GameObservation:
        return GameObservation(self.observe_board(), self.observe_state())

    @abstractmethod
    def observe_state(self) -> GameState:
        ...

    @abstractmethod
    def observe_board(self) -> BoardObservation:
        ...
