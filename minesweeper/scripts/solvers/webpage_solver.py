import sys

from src.solving.bot import BotFactory
from src.solving.strategy import StrategyFactory
from src.utils import parse_web_page_configuration


def main() -> None:
    configuration = parse_web_page_configuration(sys.argv)

    bot = BotFactory.get_webpage_bot(
        configuration.sweeper_configuration,
        StrategyFactory.get_random_strategy(),
        configuration.username
    )

    bot.solve(10, True)


if __name__ == '__main__':
    main()
