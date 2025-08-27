from typing import Tuple

from src.common import Point, Dimensions
from src.game.grids.impl.generic_grid import GenericGrid
from src.game.literals import GameState
from src.game.tiles.tile import Tile


class MineField(GenericGrid):
    def __init__(self, dimensions: Dimensions, mines: int) -> None:
        super().__init__(dimensions)
        self._mines = mines
        self._game_state: GameState = 'IN_PROGRESS'

        # TODO: plant mines

    def __getitem__(self, key: Tuple[int, int]) -> Tile:  # TODO: implement
        pass

    def uncover(self, point: Point) -> None:  # TODO: implement
        pass
