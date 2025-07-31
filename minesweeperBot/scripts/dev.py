import sys

from src.bot.dedicated.webpage_bot import WebPageBot
from src.strategy.impl.random_strategy import RandomStrategy
from utils.configuration_parser import parse_configuration


def main() -> None:
    configuration = parse_configuration(sys.argv)

    webpage_bot = WebPageBot(configuration, RandomStrategy())
    webpage_bot.solve(10, True)


if __name__ == '__main__':
    main()
