from time import time
from typing import Set, override
from random import randint

from src.common import Move, Point, SweeperConfiguration
from src.game.grids import GenericGrid, Grid, FrozenGrid
from src.game.sweeper.sweeper import GameState, Sweeper
from src.game.tiles import Tile, TranspaTile


class Minefield(Sweeper):
    def __init__(self, configuration: SweeperConfiguration) -> None:
        super().__init__(configuration)

        self._field: Grid[TranspaTile] = GenericGrid(self._configuration.dimensions, lambda: TranspaTile())
        self._start_time: int | None = None
        self._flags_placed = 0
        self._state: GameState = 'IN_PROGRESS'

    def _plant_mines(self, safe_spot: Point) -> None:
        dimensions = self._configuration.dimensions
        planted_mines: Set[Point] = set()

        for m in range(self._configuration.mines):
            new_mine = Point(
                randint(0, dimensions.width - 1),
                randint(0, dimensions.height - 1)
            )

            if safe_spot != new_mine and new_mine not in planted_mines:
                continue

            planted_mines.add(new_mine)
            self._field[new_mine].set_sign('MINE')

    def _flood_reveal(self) -> None:
        pass

    @override
    def obtain_remaining_mines(self) -> int:
        return self._configuration.mines - self._flags_placed

    @override
    def obtain_state(self) -> GameState:
        pass

    @override
    def obtain_time(self) -> int:
        return int(time()) - self._start_time

    @override
    def obtain_grid(self, old_grid: Grid[Tile] | None = None) -> Grid[Tile]:
        self._check_grid_size(old_grid)

        if old_grid is None:
            return FrozenGrid(self._field)

        for point, tile in self._field:
            symbol = tile.get_symbol()

            if symbol == 'NUMBER':
                count = tile.get_count()
                assert count is not None

                old_grid[point].set_count(count)
            else:
                old_grid[point].set_sign(symbol)

        return old_grid

    @override
    def play(self, move: Move) -> None:
        # TODO: implement
        #   - update flags
        #   - update state

        if self._start_time is None:
            self._plant_mines(move.tile)
            self._start_time = int(time())

    @override
    def reset(self) -> None:
        self._field = GenericGrid(self._configuration.dimensions, lambda: TranspaTile())
        self._start_time = None
        self._flags_placed = 0
        self._state = 'IN_PROGRESS'

    @override
    def sign_victory(self, name: str) -> None:
        pass
