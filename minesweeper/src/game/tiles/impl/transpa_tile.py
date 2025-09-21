from typing import override

from src.game.tiles import Symbol, MutableTile


class TranspaTile(MutableTile):
    def __init__(self) -> None:
        super().__init__()
        self._is_revealed = False

    @override
    def get_count(self) -> int | None:
        return super().get_count()

    @override
    def get_symbol(self) -> Symbol:
        return super().get_symbol()

    @override
    def set_symbol(self, symbol: Symbol, mines: int | None = None) -> None:
        super().set_symbol(symbol, mines)

    def set_is_revealed(self, is_revealed: bool) -> None:
        self._is_revealed = is_revealed

    def is_revealed(self) -> bool:
        return self._is_revealed

    def get_inner_symbol(self) -> Symbol:
        return super().get_symbol()

    def set_inner_sign(self, symbol: Symbol) -> None:
        pass
