from src.solving.strategy import StrategyFactory
from src.solving.strategy.evaluation import Evaluator


def main() -> None:
    evaluator = Evaluator(
        [
            ('random_1',  StrategyFactory.get_random_strategy()),
            ('random_2',  StrategyFactory.get_random_strategy()),
            ('random_3',  StrategyFactory.get_random_strategy()),
            ('random_4',  StrategyFactory.get_random_strategy()),
            ('random_5',  StrategyFactory.get_random_strategy()),
        ]
    )
    evaluator.run()


if __name__ == "__main__":
    main()
