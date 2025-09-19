from itertools import combinations
from typing import List, NamedTuple, Tuple, Set

from src.common import Move, Point, Dimensions
from src.exceptions import InvalidGameStateError
from src.game.grids import Grid, GenericGrid
from src.game.tiles import Sign, Tile, MutableTile


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


def all_possible_flag_scenarios[T: Tile](  # TODO: code polish
        grid: Grid[T],
        point: Point
) -> List[FlagScenario]:
    scenarios: List[FlagScenario] = list()

    mine_count = grid[point.x, point.y].get_count()
    assert mine_count is not None

    to_flag = mine_count - grid.count_symbol_in_neighbourhood(point.x, point.y, 'FLAG')
    if to_flag < 0:
        raise InvalidGameStateError('too many flagged tiles')

    neighbours = grid.neighbourhood_with_symbol_of(point.x, point.y, 'COVERED', 'QUESTION_MARK').to_list()

    for c in combinations([i for i in range(len(neighbours))], to_flag):
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


def is_violating[T: Tile](grid: Grid[T], point: Point) -> bool:
    for number_p, number_t in grid.neighbourhood_with_symbol_of(point.x, point.y, 'NUMBER'):
        flags_in_neighbourhood = grid.count_symbol_in_neighbourhood(number_p.x, number_p.y, 'FLAG')
        mine_count = number_t.get_count()
        assert mine_count is not None

        if flags_in_neighbourhood > mine_count:
            return True

    return False


def undo_flagging[T: Tile](grid: Grid[T], before_flagging: List[Tuple[Point, Sign]]) -> None:
    for point, sign in before_flagging:
        grid[point.x, point.y].set_sign(sign)


def try_flags_scenario[T: Tile](
        grid: Grid[T],
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


def simulate[T: Tile](  # TODO: fix & code polish
        grid: Grid[T],
        number_point: Point,
        simulation_state: SimulationState,
) -> None:
    mine_count = grid[number_point.x, number_point.y].get_count()
    assert mine_count is not None
    flags_to_simulate = mine_count - grid.count_symbol_in_neighbourhood(number_point.x, number_point.y, 'FLAG')

    if flags_to_simulate == 0:
        is_affected_by_simulation = False
        for n, _ in grid.neighbourhood_of(number_point.x, number_point.y):
            if n in simulation_state.currently_safe or n in simulation_state.currently_flagged:
                is_affected_by_simulation = True
                break

        if is_affected_by_simulation:
            for n, _ in grid.neighbourhood_with_symbol_of(number_point.x, number_point.y, 'NUMBER'):
                if n in simulation_state.currently_visiting:
                    continue

                simulation_state.currently_visiting.add(n)
                simulate(grid, n, simulation_state)
                simulation_state.currently_visiting.remove(n)
        else:
            simulation_state.accept_current()
        return

    simulation_state.currently_visiting.add(number_point)

    for flag_scenario in all_possible_flag_scenarios(grid, number_point):
        is_valid, before_flagging = try_flags_scenario(grid, flag_scenario)
        if not is_valid or before_flagging is None:
            continue

        simulation_state.currently_flagged.update(flag_scenario.flags)
        simulation_state.currently_safe.update(flag_scenario.safe)

        to_visit: Set[Point] = set()
        for p in flag_scenario.flags:
            to_visit.update([p for p, _ in grid.neighbourhood_with_symbol_of(p.x, p.y, 'NUMBER')])
        for p in flag_scenario.safe:
            to_visit.update([p for p, _ in grid.neighbourhood_with_symbol_of(p.x, p.y, 'NUMBER')])

        for p in to_visit:
            for n, _ in grid.neighbourhood_with_symbol_of(p.x, p.y, 'NUMBER'):
                if n in simulation_state.currently_visiting:
                    continue

                simulate(grid, n, simulation_state)

        undo_flagging(grid, before_flagging)

        for e in flag_scenario.flags:
            simulation_state.currently_flagged.remove(e)
        for e in flag_scenario.safe:
            if e in simulation_state.currently_safe:
                simulation_state.currently_safe.remove(e)

    simulation_state.currently_visiting.remove(number_point)


def calculate_safe_moves[T: Tile](grid: Grid[T]) -> List[Move]:
    moves: List[Move] = list()

    for point, tile in grid:
        if tile.get_symbol() != 'NUMBER':
            continue

        mines = tile.get_count()
        assert mines is not None
        flags = grid.count_symbol_in_neighbourhood(point.x, point.y, 'FLAG')

        if flags < mines:
            simulation_state = SimulationState()
            simulate(grid, point, simulation_state)

            always_flagged, always_safe = simulation_state.get_result()
            if len(always_flagged) > 0 or len(always_safe) > 0:
                for p in always_flagged:
                    moves.append(Move('FLAG', p))
                for p in always_safe:
                    moves.append(Move('UNCOVER', p))

                return moves

    return moves


def main() -> None:
    grid = GenericGrid[MutableTile](Dimensions(6, 7), lambda: MutableTile())

    for x, y in [(3, 0), (4, 0), (5, 0), (5, 6)]:
        grid[x, y].set_sign('EMPTY')
    for x, y in [(3, 1), (2, 2), (4, 6)]:
        grid[x, y].set_count(1)
    for x, y in [(2, 0), (2, 1), (4, 1), (5, 1), (1, 2), (3, 2), (2, 3), (5, 5)]:
        grid[x, y].set_count(2)
    for x, y in [(1, 3), (4, 5)]:
        grid[x, y].set_count(3)
    grid[3, 3].set_count(4)
    grid[5, 3].set_count(5)
    for x, y in [(1, 0), (1, 1), (4, 2), (5, 2), (4, 3), (4, 4), (5, 4)]:
        grid[x, y].set_sign('FLAG')

    grid.print()
    print()
    print(calculate_safe_moves(grid))


if __name__ == '__main__':
    main()
