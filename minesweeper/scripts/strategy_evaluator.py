import sys

from argparse import ArgumentParser
from enum import Enum
from typing import Dict, Final, List, Tuple

from src.common import Dimensions, SweeperConfiguration
from src.solving.bot import BotFactory
from src.solving.strategy import Strategy, StrategyFactory


STRATEGIES: Final[List[Tuple[str, Strategy]]] = [
    ('random_strategy', StrategyFactory.get_random_strategy()),
]


SQUARE_SIZE: Final = 24
BATCH_SIZE:  Final = 1000

DIMENSIONS: Final = Dimensions(
    width=SQUARE_SIZE,
    height=SQUARE_SIZE,
)


class Difficulty(Enum):
    EASY         = 8.1
    INTERMEDIATE = 6.4
    HARD         = 4.8


def evaluate_strategy(strategy_name: str, strategy: Strategy) -> Dict[Difficulty, float]:
    winrates: Dict[Difficulty, float] = dict()

    for difficulty in Difficulty:
        print(f'... evaluating {strategy_name}::{difficulty}')

        configuration = SweeperConfiguration(
            dimensions=DIMENSIONS,
            mines=int((SQUARE_SIZE ** 2) / difficulty.value),
            question_marks=False
        )

        bot = BotFactory.get_minefield_bot(configuration, strategy, 'strategy_evaluator')

        victories = bot.batch_solve(BATCH_SIZE)
        winrates[difficulty] = victories / BATCH_SIZE

    return winrates


def evaluate_strategies(strategies: List[Tuple[str, Strategy]]) -> Dict[str, Dict[Difficulty, float]]:
    return dict(
        [
            (strategy_name, evaluate_strategy(strategy_name, strategy))
            for strategy_name, strategy
            in strategies
        ]
    )


def list_evaluations(evaluation: Dict[str, Dict[Difficulty, float]]) -> None:  # TODO: implement
    pass


def order_evaluations(evaluation: Dict[str, Dict[Difficulty, float]]) -> None:  # TODO: implement
    pass


def main() -> None:
    parser = ArgumentParser(prog=sys.argv[0])
    parser.add_argument(
        '--order', '-o',
        action='store_true',
    )

    ns = parser.parse_args()

    evaluations = evaluate_strategies(STRATEGIES)
    if ns.order:
        order_evaluations(evaluations)
    else:
        list_evaluations(evaluations)


if __name__ == "__main__":
    main()
