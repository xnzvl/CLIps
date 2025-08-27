from src.game.grids.grid import Grid
from src.game.literals import Result, GameState
from src.ui.input import Input
from src.ui.ui import UI


class BlessedTUI(UI):
    def render_game_state(self, game_state: GameState) -> None:
        pass

    def render_grid(self, grid: Grid) -> None:
        pass

    def render_result(self, result: Result) -> None:
        pass

    def get_player_input(self) -> Input:
        pass
