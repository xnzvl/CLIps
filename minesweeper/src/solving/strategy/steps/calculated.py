from typing import List

from src.common import Move, Point
from src.game.grids.grid import Grid
from src.game.grids.impl.mutable_grid import MutableGrid


def calculate_safe_moves(grid: Grid) -> List[Move]:
    for point, tile in grid:
        if tile.get_symbol() != 'NUMBER':
            continue

        flag_options = grid.get_neighbours_of_tile_at(point.x, point.y)

    return list()


def _simulate_around(grid: Grid, number_point: Point) -> List[Move] | None:
    neighbours = grid.get_neighbours_of_tile_at(number_point.x, number_point.y)

    flag_count = len([None for p, t in neighbours if t.get_symbol() == 'FLAG'])
    mines = grid[number_point.x, number_point.y].get_count()
    assert mines is not None

    if flag_count > mines:
        return None

    return list()


def get_all_indices_for_n(n: int, from_i: int, to_i: int, current: List[int], result: List[List[int]]) -> None:
    if n == 0:
        result.append(current.copy())
        return

    max_i = to_i - from_i - n + 2
    for i in range(max_i):
        current.append(from_i + i)
        get_all_indices_for_n(n - 1, from_i + i + 1, to_i, current, result)
        current.pop()


def get_all_indices(n: int, max_i: int) -> List[List[int]]:
    result = list()

    for i in range(n, 0, -1):
        sub_result = list()
        get_all_indices_for_n(i, 0, max_i, list(), sub_result)
        result.extend(sub_result)

    return result


def main() -> None:
    simple_grid = MutableGrid(5, 2)
    for x in range(5):
        simple_grid[x, 1].set_count(1 if x != 1 and x != 3 else 2)

    simple_grid.print()


    trickier_grid = MutableGrid(4, 3)
    trickier_grid[0, 1].set_count(1)
    trickier_grid[1, 1].set_count(1)
    trickier_grid[2, 1].set_count(3)
    trickier_grid[0, 2].set_count(0)
    trickier_grid[1, 2].set_count(0)
    trickier_grid[2, 2].set_count(1)

    trickier_grid.print()

    print()

    for c in get_all_indices(3, 5):
        print(c)

    return


if __name__ == '__main__':
    main()
