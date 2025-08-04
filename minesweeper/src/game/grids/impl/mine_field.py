from typing import Tuple

from src.common import Point
from src.game.grids.impl.shaped_grid import ShapedGrid
from src.game.literals import GameState
from src.game.tiles.tile import Tile


class MineField(ShapedGrid):
    def __init__(self, width: int, height: int, mines: int) -> None:
        super().__init__(width, height)
        self._mines = mines
        self._game_state: GameState = 'inProgress'

        # TODO: plant mines

    def __getitem__(self, key: Tuple[int, int]) -> Tile:
        # TODO: implement
        pass

    def uncover(self, point: Point) -> None:
        # TODO: implement
        pass
