from src.game.sweeper import GameState, Minefield


class TestFixtures:
    def test_default_in_progress(self, opened_minefield) -> None:
        assert opened_minefield.obtain_state() == GameState.IN_PROGRESS

    def test_in_progress_after_opening(self, opened_minefield: Minefield) -> None:
        assert opened_minefield.obtain_state() == GameState.IN_PROGRESS

    def test_failure_minefield(self, failure_minefield: Minefield) -> None:
        assert failure_minefield.obtain_state() == GameState.FAILURE

    def test_victory_minefield(self, victory_minefield: Minefield) -> None:
        victory_minefield.obtain_grid().print()
        assert victory_minefield.obtain_state() == GameState.VICTORY
