from itertools import combinations
from typing import List, Tuple, Set

from src.common import Move, Point
from src.exceptions import InvalidGameStateError
from src.game.grids.grid import Grid
from src.game.grids.impl.mutable_grid import MutableGrid
from src.game.tiles.tile import Tile, Sign


def _all_possible_flag_scenarios(grid: Grid, point: Point) -> List[List[Tuple[Point, Tile]]]:
    scenarios: List[List[Tuple[Point, Tile]]] = list()

    mine_count = grid[point.x, point.y].get_count()
    assert mine_count is not None

    max_to_be_flagged = mine_count - grid.count_symbol_in_neighbourhood(point.x, point.y, 'FLAG')
    if max_to_be_flagged < 0:
        raise InvalidGameStateError('too many flagged tiles')

    for potential_flags in range(max_to_be_flagged, 0, -1):
        for indices in combinations(
                grid.get_neighbours_with_symbol(point.x, point.y, 'COVERED', 'QUESTION_MARK'),
                potential_flags
        ):
            scenarios.append(list(indices))

    return scenarios


def _is_violating(grid: Grid, point: Point) -> bool:
    for number_p, number_t in grid.get_neighbours_with_symbol(point.x, point.y, 'NUMBER'):
        flags_in_neighbourhood = grid.count_symbol_in_neighbourhood(number_p.x, number_p.y, 'FLAG')
        mine_count = number_t.get_count()
        assert mine_count is not None

        if flags_in_neighbourhood > mine_count:
            return True

    return False


def _undo_flagging(grid: Grid, before_flagging: List[Tuple[Point, Sign]], simulated_flags: Set[Point]) -> None:
    for point, sign in before_flagging:
        grid[point.x, point.y].set_sign(sign)
        simulated_flags.remove(point)


def _try_flags_scenario(grid: Grid, scenario: List[Tuple[Point, Tile]], simulated_flags: Set[Point]) -> List[Tuple[Point, Sign]] | None:
    before_flagging: List[Tuple[Point, Sign]] = list()

    for to_flag_point, to_flag_tile in scenario:
        before_symbol = to_flag_tile.get_symbol()
        assert before_symbol != 'NUMBER'
        before_flagging.append((to_flag_point, before_symbol))

        to_flag_tile.set_sign('FLAG')
        simulated_flags.add(to_flag_point)

        if _is_violating(grid, to_flag_point):
            _undo_flagging(grid, before_flagging, simulated_flags)
            return None

    return before_flagging


# TODO: make compatible with question marks
def _append_to_moves(moves: List[Move], scenario: List[Tuple[Point, Tile]]) -> None:
    for p, _ in scenario:
        moves.append(
            Move('secondary', p)
        )


def _undo_scenario_from_moves_stack(moves: List[Move],scenario_length: int) -> None:
    for _ in range(scenario_length):
        moves.pop()


def _simulate_around(
        grid: Grid,
        number_point: Point,
        moves_stack: List[Move],
        simulated_flags: Set[Point],
        already_visited: Set[Point]
) -> bool:


    for scenario in _all_possible_flag_scenarios(grid, number_point):
        affected_points = _try_flags_scenario(grid, scenario, simulated_flags)
        if affected_points is None:
            continue

        to_visit = set()
        for affected_point, _ in affected_points:
            to_visit.add(grid.get_neighbours_with_symbol(affected_point.x, affected_point.y, 'COVERED', 'QUESTION_MARK'))

        for to_visit_p, _ in affected_points:
            _simulate_around(grid, to_visit_p, moves_stack, simulated_flags, already_visited)

        # _append_to_moves(moves_stack, scenario)

        # for n_p, _ in grid.get_neighbours_with_symbol(number_point.x, number_point.y, 'NUMBER'):
        #     is_sim_successful = _simulate_around(grid, n_p, moves_stack, simulated_flags)

        #     if is_sim_successful:
        #         return True

        # _undo_scenario_from_moves_stack(moves_stack, len(scenario))
        # _undo_flagging(grid, affected_points, simulated_flags)

    return False


def calculate_safe_moves(grid: Grid) -> List[Move]:
    for point, tile in grid:
        if tile.get_symbol() != 'NUMBER':
            continue

        mines = tile.get_count()
        assert mines is not None
        flags = grid.count_symbol_in_neighbourhood(point.x, point.y, 'FLAG')

        if flags < mines:
            result = list()
            if _simulate_around(grid, point, result, set()):
                return result

    return list()


def main() -> None:
    simple_grid = MutableGrid(5, 2)
    for x in range(5):
        simple_grid[x, 1].set_count(1 if x != 1 and x != 3 else 2)

    # simple_grid.print()


    trickier_grid = MutableGrid(4, 3)
    trickier_grid[0, 1].set_count(1)
    trickier_grid[1, 1].set_count(1)
    trickier_grid[2, 1].set_count(3)
    trickier_grid[0, 2].set_count(0)
    trickier_grid[1, 2].set_count(0)
    trickier_grid[2, 2].set_count(1)

    trickier_grid.print()
    print()
    for m in calculate_safe_moves(trickier_grid):
        print(m)

    return


if __name__ == '__main__':
    main()
