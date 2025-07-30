import sys

from src.bots.specific.webpage_bot import WebPageBot
from src.strategies.impl.random_strategy import RandomStrategy
from utils.configuration_parser import parse_configuration


def main() -> None:
    configuration = parse_configuration(sys.argv)

    webpage_bot = WebPageBot(configuration, RandomStrategy())
    webpage_bot.solve(100)


if __name__ == '__main__':
    main()
