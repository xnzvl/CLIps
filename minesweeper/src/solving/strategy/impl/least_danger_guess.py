from random import choice
from typing import Callable, Dict, List, Tuple, override

from src.common import Action, Move, Point
from src.game.grids import Grid
from src.game.tiles import Symbol, Tile

from ..strategy import Strategy
from ..strategy_error import StrategyError


type DangerIncrementer = Callable[[Tuple[int, int], int, int], Tuple[int, int]]


class LeastDangerShallowGuess(Strategy):
    @override
    def apply[T: Tile](self, grid: Grid[T]) -> List[Move]:
        return [choice(least_danger_choices(grid, danger_shallow_incrementer))]


class LeastDangerDeeperGuess(Strategy):
    @override
    def apply[T: Tile](self, grid: Grid[T]) -> List[Move]:
        return [choice(least_danger_choices(grid, danger_deeper_incrementer))]


def danger_shallow_incrementer(danger_ratio: Tuple[int, int], count: int, flags: int) -> Tuple[int, int]:
    dangerous_neighbours, number_neighbours = danger_ratio
    return (
        dangerous_neighbours + (1 if count > flags else 0),
        number_neighbours + 1
    )


def danger_deeper_incrementer(danger_ratio: Tuple[int, int], count: int, flags: int) -> Tuple[int, int]:
    dangerous_neighbours, number_neighbours = danger_ratio
    return (
        dangerous_neighbours + max(count - flags, 0),
        number_neighbours + 1
    )


def count_flags(l: List[Tuple[Point, Tile]]) -> int:
    count = 0

    for _, tile in l:
        if tile.get_symbol() == Symbol.FLAG:
            count += 1

    return count


def calculate_danger_ratios[T: Tile](
        grid: Grid[T],
        danger_incrementer: DangerIncrementer
) -> Dict[Point, Tuple[int, int]]:
    danger_ratios: Dict[Point, Tuple[int, int]] = dict()

    for point, tile in grid:
        if tile.get_symbol() != Symbol.NUMBER:
            continue

        neighbours = grid.neighbourhood_of(point.x, point.y) \
            .to_list()
        flag_count = count_flags(neighbours)

        count = tile.get_count()
        assert count is not None
        if flag_count > count:
            raise StrategyError('invalid state - too many flags')

        for n_point, n_tile in neighbours:
            if not n_tile.is_covered():
                continue

            danger_ratios[n_point] = danger_incrementer(
                danger_ratios.get(n_point, (0, 0)), count, flag_count
            )

    return danger_ratios


def least_danger_choices[T: Tile](
        grid: Grid[T],
        danger_incrementer: DangerIncrementer
) -> List[Move]:
    danger_ratios = calculate_danger_ratios(grid, danger_incrementer)

    least_danger_moves_list: List[Move] = list()
    lowest_mine_probability = 1.0

    for point, (dangerous_neighbours, number_neighbours) in danger_ratios.items():
        mine_probability = dangerous_neighbours / number_neighbours

        if mine_probability < lowest_mine_probability:
            least_danger_moves_list.clear()
            lowest_mine_probability = mine_probability

        if mine_probability == lowest_mine_probability:
            least_danger_moves_list.append(Move(Action.UNCOVER, point))

    return least_danger_moves_list
