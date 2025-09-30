from abc import ABC, abstractmethod
from typing import Callable

from src.common import Dimensions, Dimensioned
from src.game.grids.grid import Grid
from src.game.sweeper import GameState, Result
from src.game.tiles import Tile
from src.ui.input import Input
from src.ui.repeater import Repeater


class UI(Dimensioned, ABC):
    def __init__(self, dimensions: Dimensions, username: str) -> None:  # TODO: UI should know about ? flag
        super().__init__(dimensions)

        self._username = username
        self._repeater: Repeater | None = None

    def start_rendering_time(self, time_getter: Callable[[], int]) -> None:
        if self._repeater is None:
            self._repeater = Repeater(
                1.0,
                lambda: self.render_time(time_getter()),  # TODO: handle exception from repeater? or modify repeater?
            )
            self._repeater.start()

    def stop_rendering_time(self) -> None:
        if self._repeater is not None:
            self._repeater.stop()
            self._repeater = None

    @abstractmethod
    def render_remaining_mines(self, remaining_mines: int) -> None:
        ...

    @abstractmethod
    def render_game_state(self, game_state: GameState) -> None:
        ...

    @abstractmethod
    def render_time(self, seconds: int) -> None:
        ...

    @abstractmethod
    def render_grid[T: Tile](self, grid: Grid[T]) -> None:
        ...

    @abstractmethod
    def render_result(self, result: Result) -> None:
        ...

    @abstractmethod
    def get_player_input(self, game_state: GameState) -> Input:
        ...
