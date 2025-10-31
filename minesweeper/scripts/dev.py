from src.common import Dimensions, SweeperConfiguration
from src.game.sweeper import Minefield
from src.solving.bot import Bot, logging_batch_solve
from src.solving.strategy import StrategyFactory


def main() -> None:
    bot = Bot(
        Minefield(
            SweeperConfiguration(
                Dimensions(24, 24),
                90,
                False
            )
        ),
        StrategyFactory.get_certain_strategy(),
        ''
    )

    logging_batch_solve(bot, 10)


if __name__ == '__main__':
    main()
