from src.game.symbol import Symbol


class Tile:
    def __init__(self) -> None:
        self._symbol = Symbol.COVERED
        self._count: int | None = None

    def get_count(self) -> int | None:
        return self._count

    def set_count(self, count: int) -> None:
        if count < 0:
            raise ValueError(f"number of mines in the proximity cannot be lower than 0 (received {count})")
        if count > 8:
            raise ValueError(f"number of mines in the proximity cannot be greater than 8 (received {count})")

        if count == 0:
            self._symbol = Symbol.EMPTY
            self._count = None
        else:
            self._symbol = Symbol.NUMBER
            self._count = count

    def get_symbol(self) -> Symbol:
        return self._symbol

    def set_symbol(self, symbol: Symbol) -> None:
        """
        Set the symbol of on the Tile.
        Throws ValueError on Symbol.NUMBER.
        """
        if symbol == Symbol.NUMBER:
            raise ValueError("symbol cannot be NUMBER")

        self._symbol = symbol
        self._count = None
