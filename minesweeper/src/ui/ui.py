from abc import ABC, abstractmethod

from src.game.grids.grid import Grid
from src.game.literals import GameState, Result
from src.ui.input import Input


class UI(ABC):
    @abstractmethod
    def render_game_state(self, game_state: GameState) -> None:
        ...

    @abstractmethod
    def render_remaining_mines(self, remaining_mines: int) -> None:
        pass

    @abstractmethod
    def render_grid(self, grid: Grid) -> None:
        ...

    @abstractmethod
    def render_result(self, result: Result) -> None:
        ...

    @abstractmethod
    def get_player_input(self) -> Input:
        ...
