from src.solving.strategy import Strategy
from src.solving.strategy.steps import LeastDangerGuess, RandomStep, CertainStep


class StrategyFactory:
    @staticmethod
    def get_random_strategy() -> Strategy:
        return Strategy(
            [
                RandomStep()
            ]
        )

    @staticmethod
    def get_certain_strategy() -> Strategy:
        return Strategy(
            [
                CertainStep(),
                RandomStep()
            ]
        )

    @staticmethod
    def get_least_danger_strategy() -> Strategy:
        return Strategy(
            [
                CertainStep(),
                LeastDangerGuess(),
                RandomStep()
            ]
        )
