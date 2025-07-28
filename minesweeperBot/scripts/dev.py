import sys

from src.game.board import Board
from src.interactions.webpage.webpage_observer import WebPageObserver
from utils.configuration_parser import parse_configuration


def main() -> None:
    configuration = parse_configuration(sys.argv)
    observer = WebPageObserver(configuration)

    b = Board(configuration.dimensions.width, configuration.dimensions.height)

    for p, t in b:
        print(p)


if __name__ == '__main__':
    main()
