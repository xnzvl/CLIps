import sys

from src.solving.bot.impl.webpage_bot import WebPageBot
from src.solving.strategy.impl.calculated_strategy import CalculatedStrategy
from src.utils.configuration_parser import parse_configuration


def main() -> None:
    configuration = parse_configuration(sys.argv)

    webpage_bot = WebPageBot(configuration, CalculatedStrategy(), False)
    webpage_bot.solve(10, False)


if __name__ == '__main__':
    main()
