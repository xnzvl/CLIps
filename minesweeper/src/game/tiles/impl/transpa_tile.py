from typing import override

from src.game.tiles import Symbol, MutableTile


class TranspaTile(MutableTile):
    def __init__(self) -> None:
        super().__init__()
        self._is_transparent = True

    @override
    def get_count(self) -> int | None:
        return None if self._is_transparent else super().get_count()

    @override
    def get_symbol(self) -> Symbol:
        return 'COVERED' if self._is_transparent else super().get_symbol()

    def set_transparency(self, transparency: bool) -> None:
        self._is_transparent = transparency