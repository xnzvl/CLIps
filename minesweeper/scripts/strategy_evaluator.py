from src.solving.strategy import StrategyFactory
from src.solving.strategy.evaluation import Evaluator


def main() -> None:
    evaluator = Evaluator(
        [
            ('random',            StrategyFactory.get_random_strategy()           ),
            ('certain',           StrategyFactory.get_certain_strategy()          ),
            # ('least_danger',      StrategyFactory.get_least_danger_strategy()     ),
            # ('least_danger_plus', StrategyFactory.get_least_danger_strategy_plus()),
        ],
        testing_batch_size=126,
    )
    evaluator.run()


if __name__ == "__main__":
    main()
