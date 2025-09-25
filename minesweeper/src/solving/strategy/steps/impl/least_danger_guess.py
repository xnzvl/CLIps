from random import choice
from typing import Dict, List, Tuple, override

from src.common import Action, Move, Point
from src.game.grids import Grid
from src.game.tiles import Symbol, Tile
from src.solving.strategy.steps import Step


class LeastDangerGuess(Step):
    @override
    def get_moves[T: Tile](self, grid: Grid[T]) -> List[Move]:
        return [choice(LeastDangerGuess.least_danger_choices(grid))]

    @staticmethod
    def calculate_mine_probabilities[T: Tile](grid: Grid[T]) -> Dict[Point, Tuple[int, int]]:
        mine_probabilities: Dict[Point, Tuple[int, int]] = dict()

        for point, tile in grid:
            if tile.get_symbol() != Symbol.NUMBER:
                continue

            neighbours = grid.neighbourhood_of(point.x, point.y)
            flag_count = grid.count_symbol_in_neighbourhood(point.x, point.y, Symbol.FLAG)

            count = tile.get_count()
            assert count is not None
            if flag_count > count:
                raise RuntimeError('invalid state - too many flags')  # TODO: better exception

            are_mines_around = flag_count < count
            for n_point, n_tile in neighbours:
                symbol = n_tile.get_symbol()

                if symbol == Symbol.COVER or symbol == Symbol.QUESTION_MARK:
                    dangerous_neighbours, number_neighbours = mine_probabilities.get(n_point, (0, 0))
                    mine_probabilities[n_point] = (
                        dangerous_neighbours + (1 if are_mines_around else 0),
                        number_neighbours + 1
                    )

        return mine_probabilities

    @staticmethod
    def least_danger_choices[T: Tile](grid: Grid[T]) -> List[Move]:
        mine_probabilities = LeastDangerGuess.calculate_mine_probabilities(grid)

        least_danger_moves_list: List[Move] = list()
        lowest_mine_probability = 1.0
        for point, (dangerous_neighbours, number_neighbours) in mine_probabilities.items():
            mine_probability = dangerous_neighbours / number_neighbours

            if mine_probability < lowest_mine_probability:
                least_danger_moves_list.clear()
                lowest_mine_probability = mine_probability

            if mine_probability == lowest_mine_probability:
                least_danger_moves_list.append(Move(Action.UNCOVER, point))

        return least_danger_moves_list
