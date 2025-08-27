from typing import override

from src.common import Dimensions
from src.game.grids.grid import Grid
from src.game.literals import Result, GameState
from src.ui.input import Input
from src.ui.ui import UI


class BlessedTUI(UI):
    def __init__(self, dimensions: Dimensions, mines: int) -> None:
        pass

    @override
    def render_game_state(self, game_state: GameState) -> None:
        pass

    @override
    def render_remaining_mines(self, remaining_mines: int) -> None:
        pass

    @override
    def render_grid(self, grid: Grid) -> None:
        pass

    @override
    def render_result(self, result: Result) -> None:
        pass

    @override
    def get_player_input(self) -> Input:
        pass
