from random import choice
from typing import Dict, List, Tuple, override

from src.common import Action, Move, Point
from src.game.grids import Grid
from src.game.tiles import Symbol, Tile

from ..strategy import Strategy
from ..strategy_error import StrategyError


class SafestRandomStep(Strategy):
    @override
    def apply[T: Tile](self, grid: Grid[T]) -> List[Move]:
        options = safest_options(grid)

        return [choice(options)] \
            if len(options) > 0 \
            else []


def compute_danger_ratios[T: Tile](grid: Grid[T]) -> Dict[Point, Tuple[int, int]]:
    danger_ratios: Dict[Point, Tuple[int, int]] = dict()

    for point, tile in grid:
        if tile.get_symbol() != Symbol.NUMBER:
            continue

        available_covers = grid.count_symbol_in_neighbourhood(point.x, point.y, Symbol.COVER, Symbol.QUESTION_MARK)
        flags = grid.count_symbol_in_neighbourhood(point.x, point.y, Symbol.FLAG)
        mines_to_be_placed = tile.get_count() - flags

        if mines_to_be_placed > available_covers or mines_to_be_placed < 0:
            raise StrategyError('invalid state of the grid')
        if mines_to_be_placed == 0:
            continue

        for neighbourhood_point, neighbourhood_tile in grid.neighbourhood_with_symbol_of(point.x, point.y, Symbol.COVER, Symbol.QUESTION_MARK):
            x, y = danger_ratios.get(neighbourhood_point, (0, 0))
            danger_ratios[neighbourhood_point] = (x + mines_to_be_placed, y + available_covers)

    return danger_ratios


def safest_options[T: Tile](grid: Grid[T]) -> List[Move]:
    minimal_danger_moves: List[Move] = list()
    minimal_danger = 1.0

    for point, (measured_danger, max_danger) in compute_danger_ratios(grid).items():
        danger = measured_danger / max_danger

        if danger < minimal_danger:
            minimal_danger = danger
            minimal_danger_moves.clear()

        if danger == minimal_danger:
            minimal_danger_moves.append(
                Move(
                    action=Action.UNCOVER,
                    point=point
                )
            )

    return minimal_danger_moves
