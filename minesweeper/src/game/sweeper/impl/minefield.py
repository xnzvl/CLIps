from time import time
from typing import List, Literal, Set, override
from random import randint

from src.common import Move, Point, SweeperConfiguration
from src.game.grids import FrozenGrid, GenericGrid, Grid
from src.game.sweeper import GameState, Sweeper
from src.game.tiles import Tile, RevealTile, Symbol


CoverModifierSymbol = Literal[
    Symbol.COVER,
    Symbol.QUESTION_MARK,
    Symbol.FLAG
]


class Minefield(Sweeper[SweeperConfiguration]):
    def __init__(self, configuration: SweeperConfiguration) -> None:
        super().__init__(configuration)

        self._field: Grid[RevealTile] = GenericGrid(self._configuration.dimensions, RevealTile)

        self._planted_mines: Set[Point] = set()
        self._start_time: int | None = None

        self._to_uncover = configuration.dimensions.width * configuration.dimensions.height - configuration.mines
        self._flags_placed = 0

        self._state: GameState = GameState.IN_PROGRESS

    def _plant_mines(self, safe_spot: Point) -> None:
        width, height = self._configuration.dimensions.width, self._configuration.dimensions.height

        for m in range(self._configuration.mines):
            new_mine = Point(
                randint(0, width - 1),
                randint(0, height - 1)
            )

            if safe_spot != new_mine and new_mine not in self._planted_mines:
                continue

            self._planted_mines.add(new_mine)
            self._field[new_mine].set_symbol(Symbol.MINE)

    def _uncover_flood(self, start: Point) -> None:
        to_visit: List[Point] = [start]
        marked_to_visit: Set[Point] = {start}

        while len(to_visit) > 0:
            point = to_visit.pop()
            tile = self._field[point]

            tile.reveal()
            self._to_uncover -= 1

            if tile.get_symbol() != Symbol.EMPTY:
                continue
            for n, _ in self._field.neighbourhood_of(point.x, point.y):
                if n not in marked_to_visit:
                    to_visit.append(n)
                    marked_to_visit.add(n)

    def _reveal_other_mines(self) -> None:
        for point in self._planted_mines:
            self._field[point].reveal()

    def _uncover_point(self, point: Point) -> None:
        # assumes that tile at point is covered

        tile = self._field[point]

        if tile.get_symbol() == Symbol.FLAG:
            return

        match tile.get_data_symbol():
            case Symbol.NUMBER:
                tile.reveal()
                self._to_uncover -= 1
            case Symbol.EMPTY:
                self._uncover_flood(point)
            case Symbol.MINE:
                tile.reveal(True)
                self._reveal_other_mines()
                self._state = GameState.FAILURE

    def _modify_tile_cover(self, point: Point, new_symbol: CoverModifierSymbol) -> None:
        # assumes that tile at point is covered

        tile = self._field[point]
        old_symbol = tile.get_symbol()

        if old_symbol == Symbol.FLAG and new_symbol != Symbol.FLAG:
            self._flags_placed -= 1
        elif old_symbol != Symbol.FLAG and new_symbol == Symbol.FLAG:
            self._flags_placed += 1

        tile.set_symbol(new_symbol)

    @override
    def obtain_remaining_mines(self) -> int:
        return self._configuration.mines - self._flags_placed

    @override
    def obtain_state(self) -> GameState:
        return self._state

    @override
    def obtain_time(self) -> int:
        return (int(time()) - self._start_time) if self._start_time is not None else 0

    @override
    def obtain_grid(self, old_grid: Grid[Tile] | None = None) -> Grid[Tile]:
        if old_grid is None:
            return FrozenGrid(self._field)

        self._check_grid_size(old_grid)

        for point, tile in self._field:
            symbol = tile.get_symbol()

            if symbol == Symbol.NUMBER:
                count = tile.get_count()
                assert count is not None

                old_grid[point].set_symbol(symbol, count)
            else:
                old_grid[point].set_symbol(symbol)

        return old_grid

    @override
    def play(self, move: Move) -> None:
        point = move.point

        if not self._field[point].is_covered():
            return

        match move.action:
            case 'UNCOVER':
                self._uncover_point(point)
            case 'FLAG':
                self._modify_tile_cover(point, Symbol.FLAG)
            case 'QUESTION_MARK':
                self._modify_tile_cover(point, Symbol.QUESTION_MARK)
            case 'CLEAR':
                self._modify_tile_cover(point, Symbol.COVER)

        if self._start_time is None:
            self._plant_mines(move.point)
            self._start_time = int(time())

    @override
    def reset(self) -> None:
        configuration = self._configuration

        self._field = GenericGrid(configuration.dimensions, RevealTile)

        self._planted_mines.clear()
        self._start_time = None

        self._to_uncover = configuration.dimensions.width * configuration.dimensions.height - configuration.mines
        self._flags_placed = 0

        self._state = GameState.IN_PROGRESS

    @override
    def sign_victory(self, name: str) -> None:  # TODO: impl
        pass
