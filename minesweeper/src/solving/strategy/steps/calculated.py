from itertools import combinations
from typing import List, NamedTuple, Tuple, Set

from src.common import Move, Point
from src.exceptions import InvalidGameStateError
from src.game.grids.grid import Grid
from src.game.grids.impl.mutable_grid import MutableGrid
from src.game.tiles.tile import Tile, Sign


class _SimulationState(NamedTuple):
    currently_safe: Set[Point]
    currently_flagged: Set[Point]
    always_safe: Set[Point]
    always_flagged: Set[Point]


def all_possible_flag_scenarios(grid: Grid, point: Point) -> List[List[Tuple[Point, Tile]]]:
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


def try_flags_scenario(
        grid: Grid,
        scenario: List[Tuple[Point, Tile]]
) -> Tuple[List[Tuple[Point, Sign]], List[Point]] | None:
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


def _simulate(
        grid: Grid,
        number_point: Point,
        simulation_state: _SimulationState,
) -> bool:
    mine_count = grid[number_point.x, number_point.y].get_count()
    assert mine_count is not None
    flags_to_simulate = mine_count - len(
        grid.get_neighbours_with_symbol(number_point.x, number_point.y, 'FLAG')
    )

    if flags_to_simulate == 0:
        # intersect current and always sim substates
        return True

    at_least_one_valid_scenario = False
    for flag_scenario in all_possible_flag_scenarios(grid, number_point):
        before_flagging = try_flags_scenario(grid, flag_scenario, simulation_state)
        if before_flagging is None:
            continue

        for p, _ in flag_scenario:
            is_valid_scenario = _simulate(grid, p, simulation_state)
            at_least_one_valid_scenario = at_least_one_valid_scenario or is_valid_scenario

        _undo_flagging(grid, before_flagging, simulation_state)

    return at_least_one_valid_scenario


def calculate_safe_moves(grid: Grid) -> List[Move]:
    for point, tile in grid:
        if tile.get_symbol() != 'NUMBER':
            continue

        mines = tile.get_count()
        assert mines is not None
        flags = grid.count_symbol_in_neighbourhood(point.x, point.y, 'FLAG')

        if flags < mines:
            result = list()
            if _simulate(grid, point, result, set()):
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
