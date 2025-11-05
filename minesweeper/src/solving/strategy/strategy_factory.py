from .impl.certain_step       import CertainStep
from .impl.composite_strategy import CompositeStrategy
from .impl.foresight_step     import ForesightStep
from .impl.safest_random_step import SafestRandomStep
from .impl.random_step        import RandomStep
from .strategy import Strategy


class StrategyFactory:
    @staticmethod
    def get_random_strategy() -> Strategy:
        return RandomStep()

    @staticmethod
    def get_certain_strategy() -> Strategy:
        return CompositeStrategy(
            [
                CertainStep(),
                RandomStep()
            ]
        )

    @staticmethod
    def get_least_danger_strategy() -> Strategy:
        return CompositeStrategy(
            [
                CertainStep(),
                SafestRandomStep(),
                RandomStep()
            ]
        )

    @staticmethod
    def get_foresight_strategy() -> Strategy:
        return CompositeStrategy(
            [
                CertainStep(),
                ForesightStep(),
                RandomStep()
            ]
        )
