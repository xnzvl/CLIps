from src.common import Action, SweeperConfiguration
from src.game.grids import GenericGrid, Grid
from src.game.sweeper import GameState, Sweeper
from src.game.tiles import MutableTile, Tile
from src.ui.ui import UI


class Runner:
    def __init__(self, ui: UI, sweeper: Sweeper[SweeperConfiguration]) -> None:
        self._ui = ui
        self._sweeper = sweeper

        # TODO: check if UI and Sweeper are compatible

        self._grid_cache: Grid[Tile] = GenericGrid(sweeper.get_dimensions(), lambda: MutableTile())

    def go(self) -> None:
        while True:
            game_state = self._update_ui()
            player_input = self._ui.get_player_input(game_state)

            if player_input.action == Action.RESET:
                self._sweeper.reset()

            elif player_input.action == Action.QUIT:
                break

            else:
                move = player_input.move
                assert move is not None
                self._sweeper.play(move)

    def _update_ui(self) -> GameState:
        game_state = self._sweeper.obtain_state()

        # TODO: remove comments
        self._ui.render_remaining_mines(17) # self._sweeper.obtain_remaining_mines())
        self._ui.render_game_state(game_state)
        self._ui.render_time(137) # self._sweeper.obtain_time())

        current_grid = self._sweeper.obtain_grid()
        self._ui.render_grid(current_grid)
        self._grid_cache = current_grid

        if game_state != GameState.IN_PROGRESS:
            self._ui.render_result(game_state)

        return game_state
