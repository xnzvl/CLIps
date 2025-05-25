import pyautogui as pag

from src.common import Configuration, Move
from src.interactions.clicker import Clicker


class WebPageClicker(Clicker):
    def __init__(self, configuration: Configuration) -> None:
        super().__init__(configuration)

    def do(self, move: Move) -> None:
        pag.click(
            x=self._offsets.x + move.tile.x * self._tile_size + self._tile_size // 2,
            y=self._offsets.y + move.tile.y * self._tile_size + self._tile_size // 2,
            button=move.button
        )
