from src.common import Action, SweeperConfiguration
from src.game.grids import GenericGrid, Grid
from src.game.sweeper import GameState, Sweeper
from src.game.tiles import MutableTile, Tile
from src.ui.ui import UI


class Runner:
    def __init__(self, sweeper: Sweeper[SweeperConfiguration], ui: UI) -> None:
        self._sweeper = sweeper
        self._ui = ui

        # TODO: check if UI and Sweeper are compatible

        self._grid_cache: Grid[Tile] = GenericGrid(sweeper.get_dimensions(), MutableTile)

    def run(self) -> None:
        self._ui.start_rendering_time(self._sweeper.obtain_time)

        should_run = True

        while should_run:
            game_state = self._update_ui()
            if game_state != GameState.IN_PROGRESS:
                self._ui.stop_rendering_time()

            player_input = self._ui.get_player_input(game_state)
            match player_input.action:
                case Action.RESET:
                    self._ui.start_rendering_time(self._sweeper.obtain_time)
                    self._sweeper.reset()
                case Action.QUIT:
                    self._ui.stop_rendering_time()
                    should_run = False
                case _:
                    move = player_input.move
                    assert move is not None
                    self._sweeper.play(move)

    def _update_ui(self) -> GameState:
        game_state = self._sweeper.obtain_state()

        self._ui.render_remaining_mines(self._sweeper.obtain_remaining_mines())
        self._ui.render_game_state(game_state)

        current_grid = self._sweeper.obtain_grid()
        self._ui.render_grid(current_grid)
        self._grid_cache = current_grid

        if game_state != GameState.IN_PROGRESS:
            self._ui.render_result(game_state)

        return game_state
