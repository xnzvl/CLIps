from src.game.grids.impl.generic_grid import GenericGrid
from src.game.sweeper.sweeper import GameState, Sweeper
from src.ui.ui import UI


class Runner:
    def __init__(self, ui: UI, sweeper: Sweeper) -> None:
        self._ui = ui
        self._sweeper = sweeper

        self._grid_cache = GenericGrid(sweeper.get_dimensions())

    def go(self) -> None:
        while True:
            game_state = self._update_ui()
            player_input = self._ui.get_player_input(game_state)

            if player_input.type == 'MOVE':
                move = player_input.move
                assert move is not None
                self._sweeper.play(move)

            elif player_input.type == 'RESET':
                self._sweeper.reset()

            elif player_input.type == 'QUIT':
                break

    def _update_ui(self) -> GameState:
        game_state = self._sweeper.obtain_state()

        self._ui.render_remaining_mines(self._sweeper.obtain_remaining_mines())
        self._ui.render_game_state(game_state)
        self._ui.render_time(self._sweeper.obtain_time())

        current_grid = self._sweeper.obtain_grid()
        self._ui.render_grid(current_grid)
        self._grid_cache = current_grid

        if game_state != 'IN_PROGRESS':
            self._ui.render_result(game_state)

        return game_state
