from itertools import combinations
from typing import List, NamedTuple, Tuple, Set

from src.common import Move, Point
from src.exceptions import InvalidGameStateError
from src.game.grids.grid import Grid
from src.game.grids.impl.mutable_grid import MutableGrid
from src.game.tiles.tile import Sign


class SimulationState:
    def __init__(self) -> None:
        self._possibly_safe: Set[Point] = set()
        self._flaggable: Set[Point] = set()
        self._longest_scenario = 0

        self.currently_safe: Set[Point] = set()
        self.currently_flagged: Set[Point] = set()

        self.currently_visiting: Set[Point] = set()

    def accept_current(self) -> None:
        scenario_length = len(self.currently_safe) + len(self.currently_flagged)
        if scenario_length > self._longest_scenario:
            self._possibly_safe.clear()
            self._flaggable.clear()
            self._longest_scenario = scenario_length

        if scenario_length == self._longest_scenario:
            self._possibly_safe.update(self.currently_safe)
            self._flaggable.update(self.currently_flagged)

    def get_result(self) -> Tuple[Set[Point], Set[Point]]:
        always_flagged = self._flaggable.difference(self._possibly_safe)
        always_safe = self._possibly_safe.difference(self._flaggable)
        return always_flagged, always_safe


class FlagScenario(NamedTuple):
    flags: List[Point]
    safe: List[Point]


def all_possible_flag_scenarios(  # TODO: code polish
        grid: Grid,
        point: Point
) -> List[FlagScenario]:
    scenarios: List[FlagScenario] = list()

    mine_count = grid[point.x, point.y].get_count()
    assert mine_count is not None

    max_to_be_flagged = mine_count - grid.count_symbol_in_neighbourhood(point.x, point.y, 'FLAG')
    if max_to_be_flagged < 0:
        raise InvalidGameStateError('too many flagged tiles')

    neighbours = grid.get_neighbours_with_symbol(point.x, point.y, 'COVERED', 'QUESTION_MARK')

    for c in combinations([i for i in range(len(neighbours))], max_to_be_flagged):
        safe_indices = [True for _ in range(len(neighbours))]

        for flag_i in c:
            safe_indices[flag_i] = False

        safe: List[Point] = list()
        flagged: List[Point] = list()

        for i, is_safe in enumerate(safe_indices):
            p, _ = neighbours[i]
            if is_safe:
                safe.append(p)
            else:
                flagged.append(p)

        scenarios.append(FlagScenario(flagged, safe))

    return scenarios


def is_violating(grid: Grid, point: Point) -> bool:
    for number_p, number_t in grid.get_neighbours_with_symbol(point.x, point.y, 'NUMBER'):
        flags_in_neighbourhood = grid.count_symbol_in_neighbourhood(number_p.x, number_p.y, 'FLAG')
        mine_count = number_t.get_count()
        assert mine_count is not None

        if flags_in_neighbourhood > mine_count:
            return True

    return False


def undo_flagging(grid: Grid, before_flagging: List[Tuple[Point, Sign]]) -> None:
    for point, sign in before_flagging:
        grid[point.x, point.y].set_sign(sign)


def try_flags_scenario(
        grid: Grid,
        flag_scenario: FlagScenario
) -> Tuple[bool, List[Tuple[Point, Sign]] | None]:
    before_flagging: List[Tuple[Point, Sign]] = list()

    for to_flag_point in flag_scenario.flags:
        tile = grid[to_flag_point.x, to_flag_point.y]
        before_symbol = tile.get_symbol()
        assert before_symbol != 'NUMBER'
        before_flagging.append((to_flag_point, before_symbol))

        tile.set_sign('FLAG')

        if is_violating(grid, to_flag_point):
            undo_flagging(grid, before_flagging)
            return False, None

    return True, before_flagging


def simulate(  # TODO: code polish
        grid: Grid,
        number_point: Point,
        simulation_state: SimulationState,
) -> bool:
    mine_count = grid[number_point.x, number_point.y].get_count()
    assert mine_count is not None
    flags_to_simulate = mine_count - len(
        grid.get_neighbours_with_symbol(number_point.x, number_point.y, 'FLAG')
    )

    if flags_to_simulate == 0:
        simulation_state.accept_current()
        return True

    simulation_state.currently_visiting.add(number_point)

    at_least_one_valid_scenario = False
    for flag_scenario in all_possible_flag_scenarios(grid, number_point):
        is_valid, before_flagging = try_flags_scenario(grid, flag_scenario)
        if not is_valid or before_flagging is None:
            continue

        simulation_state.currently_flagged.update(flag_scenario.flags)
        simulation_state.currently_safe.update(flag_scenario.safe)

        for p in flag_scenario.flags:
            for n, _ in grid.get_neighbours_with_symbol(p.x, p.y, 'NUMBER'):
                if n in simulation_state.currently_visiting:
                    continue

                is_valid_scenario = simulate(grid, n, simulation_state)
                at_least_one_valid_scenario = at_least_one_valid_scenario or is_valid_scenario

        undo_flagging(grid, before_flagging)

        for e in flag_scenario.flags:
            simulation_state.currently_flagged.remove(e)
        for e in flag_scenario.safe:
            if e in simulation_state.currently_safe:
                simulation_state.currently_safe.remove(e)

    simulation_state.currently_visiting.remove(number_point)
    return at_least_one_valid_scenario


def calculate_safe_moves(grid: Grid) -> List[Move]:
    for point, tile in grid:
        if tile.get_symbol() != 'NUMBER':
            continue

        mines = tile.get_count()
        assert mines is not None
        flags = grid.count_symbol_in_neighbourhood(point.x, point.y, 'FLAG')

        if flags < mines:
            simulation_state = SimulationState()

            simulation_result = simulate(grid, point, simulation_state)
            if not simulation_result:
                continue

            always_flagged, always_safe = simulation_state.get_result()
            if len(always_flagged) > 0 or len(always_safe) > 0:
                print(f'always_flagged: {always_flagged}')
                print(f'always_safe:    {always_safe}')

                return list()  # TODO: return moves

    return list()


def main() -> None:
    grid_a = MutableGrid(5, 2)
    for x in range(5):
        grid_a[x, 1].set_count(1 if x != 1 and x != 3 else 2)
    grid_a.print()
    calculate_safe_moves(grid_a)

    print()

    grid_b = MutableGrid(4, 3)
    grid_b[0, 1].set_count(1)
    grid_b[1, 1].set_count(1)
    grid_b[2, 1].set_count(3)
    grid_b[0, 2].set_count(0)
    grid_b[1, 2].set_count(0)
    grid_b[2, 2].set_count(1)
    grid_b.print()
    calculate_safe_moves(grid_b)

    print()

    grid_c = MutableGrid(3, 2)
    for x in range(3):
        grid_c[x, 1].set_count(1 if x != 1 else 2)
    grid_c.print()
    calculate_safe_moves(grid_c)

    return


if __name__ == '__main__':
    main()
