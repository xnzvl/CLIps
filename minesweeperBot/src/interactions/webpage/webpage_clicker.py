import pyautogui as pag

from src.common import Configuration, Move
from src.interactions.clicker import Clicker
from src.interactions.webpage import TILE_SIZE, SMILEY_WIDTH, SMILEY_Y_OFFSET


class WebPageClicker(Clicker):
    def __init__(self, configuration: Configuration) -> None:
        super().__init__(configuration)

    def do(self, move: Move) -> None:
        pag.click(
            x=self._offsets.x + move.tile.x * TILE_SIZE + TILE_SIZE // 2,
            y=self._offsets.y + move.tile.y * TILE_SIZE + TILE_SIZE // 2,
            button=move.button
        )

    def reset(self) -> None:
        x = self._offsets.x + (self._dimensions.width * TILE_SIZE - SMILEY_WIDTH) // 2
        y = self._offsets.y - SMILEY_Y_OFFSET

        pag.leftClick(x, y)
