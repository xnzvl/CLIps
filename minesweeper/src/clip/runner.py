from src.mediator.mediator import Mediator
from src.ui.ui import UI


class Runner:
    def __init__(self, ui: UI, mediator: Mediator) -> None:
        self._ui = ui
        self._mediator = mediator

        self._grid = mediator.observe_grid()

    def go(self) -> None:
        player_input = self._ui.get_player_input()

        while player_input.type != 'QUIT':
            if player_input.type == 'RESET':
                self._mediator.reset()
            else:
                move = player_input.move
                assert move is not None

                self._mediator.play(move)

            self._update_ui()

            player_input = self._ui.get_player_input()

    def _update_ui(self) -> None:
        game_state = self._mediator.observe_state()

        self._ui.render_game_state(self._mediator.observe_state())
        self._grid = self._mediator.observe_grid(self._grid)
        self._ui.render_grid(self._grid)

        if game_state != 'IN_PROGRESS':
            self._ui.render_result(game_state)
