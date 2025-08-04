import sys

from src.solving.bot.impl.webpage_bot import WebPageBot
from src.solving.strategy.impl.certain_first_strategy import CertainFirstStrategy
from src.utils.configuration_parser import parse_configuration


def main() -> None:
    configuration = parse_configuration(sys.argv)

    webpage_bot = WebPageBot(configuration, CertainFirstStrategy())
    webpage_bot.solve(10, True)


if __name__ == '__main__':
    main()
