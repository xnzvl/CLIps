from src.game.tiles.tile import Tile, Sign, Symbol


class TwoFaceTile(Tile):
    def __init__(self) -> None:
        self._is_mine = False

    def get_count(self) -> int | None:
        pass

    def set_count(self, count: int) -> None:
        pass

    def get_symbol(self) -> Symbol:
        pass

    def set_sign(self, sign: Sign) -> None:
        pass

    def plant_mine(self) -> None:
        self._is_mine = True
