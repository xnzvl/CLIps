from typing import override

from src.game.tiles import MineCount, Symbol, Tile


class MutableTile(Tile):
    def __init__(self) -> None:
        self._symbol: Symbol = Symbol.COVER
        self._mine_count: MineCount | None = None

    @override
    def get_count(self) -> MineCount | None:
        return self._mine_count

    @override
    def get_symbol(self) -> Symbol:
        return self._symbol

    @override
    def set_symbol(self, symbol: Symbol, mines: MineCount | None = None) -> None:
        if symbol == Symbol.NUMBER:
            assert mines is not None
        else:
            assert mines is None

        self._symbol = symbol
        self._mine_count = mines
