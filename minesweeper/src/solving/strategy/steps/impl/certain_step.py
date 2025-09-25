from typing import List, Set, Tuple, override

from src.common import Action, Move, Point
from src.game.grids import Grid
from src.game.tiles import Symbol, Tile
from src.solving.strategy.steps import Step


class CertainStep(Step):  # TODO: implement fix_certain_wrong_flags() or smth like that
    @override
    def get_moves[T: Tile](self, grid: Grid[T]) -> List[Move]:
        certain_moves: List[Move] = CertainStep.certain_flags(grid)
        certain_moves.extend(CertainStep.certain_uncovers(grid))

        return certain_moves

    @staticmethod
    def flag_neighbours[T: Tile](covered_neighbours: List[Tuple[Point, T]], flag_moves: List[Move], already_flagged: Set[Point]) -> None:
        for p, t in covered_neighbours:
            covered_symbol = t.get_symbol()

            if p in already_flagged or covered_symbol == Symbol.FLAG:
                continue

            flag_moves.append(Move(Action.FLAG, p))

            already_flagged.add(p)
            t.set_symbol(Symbol.FLAG)

    @staticmethod
    def certain_flags[T: Tile](grid: Grid[T]) -> List[Move]:
        flag_moves: List[Move] = list()
        already_flagged: Set[Point] = set()

        for point, tile in grid:
            if tile.get_symbol() != Symbol.NUMBER:
                continue

            covered_neighbours = [
                (p, t)
                for p, t in grid.neighbourhood_of(point.x, point.y)
                if t.is_covered()
            ]
            count = tile.get_count()
            assert count is not None

            if len(covered_neighbours) != count:
                continue

            CertainStep.flag_neighbours(covered_neighbours, flag_moves, already_flagged)

        return flag_moves

    @staticmethod
    def certain_uncovers[T: Tile](grid: Grid[T]) -> List[Move]:
        safe_moves: List[Move] = list()

        for point, tile in grid:
            if tile.get_symbol() != Symbol.NUMBER:
                continue

            covered_neighbours: List[Tuple[Point, Tile]] = list()
            neighbour_flags = 0

            for p, t in grid.neighbourhood_of(point.x, point.y):
                symbol = t.get_symbol()
                if symbol == Symbol.COVER or symbol == Symbol.QUESTION_MARK:
                    covered_neighbours.append((p, t))
                elif symbol == Symbol.FLAG:
                    neighbour_flags += 1

            count = tile.get_count()
            if neighbour_flags == count:
                safe_moves.extend([Move(Action.UNCOVER, p) for p, _ in covered_neighbours])

        return safe_moves
