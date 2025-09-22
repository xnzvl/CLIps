from typing import Literal, assert_never, overload, override

from src.game.tiles import Symbol, Tile


DataSymbol = Literal[
    Symbol.NUMBER,
    Symbol.EMPTY,
    Symbol.MINE
]
OuterSymbol = Literal[
    Symbol.COVER,
    Symbol.QUESTION_MARK,
    Symbol.FLAG
]


class RevealTile(Tile):
    def __init__(self) -> None:
        self._is_revealed = False
        self._revealed_by_touch = True

        self._outer_symbol: OuterSymbol = Symbol.COVER

        self._data_symbol: DataSymbol = Symbol.EMPTY
        self._data_count: int | None = None

    @override
    def get_count(self) -> int | None:
        return self._data_count if self._is_revealed else None

    @override
    def get_symbol(self) -> Symbol:
        if not self._is_revealed:
            return self._outer_symbol

        match self._data_symbol:
            case Symbol.EMPTY | Symbol.NUMBER:
                return self._data_symbol
            case Symbol.MINE:
                return Symbol.EXPLODED_MINE if self._revealed_by_touch else Symbol.MINE

        assert_never(self._data_symbol)

    @override
    def set_symbol(self, symbol: Symbol, mines: int | None = None) -> None:
        match symbol:
            case Symbol.FLAG | Symbol.QUESTION_MARK | Symbol.COVER:
                self._outer_symbol = symbol
            case _:
                raise RuntimeError(f"Invalid symbol: {symbol}")

    def reveal(self, by_touch: bool = False) -> None:
        self._is_revealed = True
        self._revealed_by_touch = by_touch

    def get_data_symbol(self) -> DataSymbol:
        return self._data_symbol

    @overload
    def set_data_symbol(self, data_symbol: Literal[Symbol.NUMBER], mines: int) -> None:
        ...

    @overload
    def set_data_symbol(self, data_symbol: Literal[Symbol.EMPTY, Symbol.MINE], mines: Literal[None]) -> None:
        ...

    def set_data_symbol(self, data_symbol: DataSymbol, mines: int | None = None) -> None:
        if data_symbol == Symbol.NUMBER:
            assert mines is not None
            Tile._check_mine_count(mines)

        self._data_symbol = data_symbol
        self._data_count = mines
