import sys

import pyautogui as pag

from src.game.board import Board
from src.interactions.webpage.webpage_observer import WebPageObserver
from utils.configuration_parser import parse_configuration


def main() -> None:
    configuration = parse_configuration(sys.argv)
    observer = WebPageObserver(configuration)

    b = Board(configuration.dimensions.width, configuration.dimensions.height)
    observer.observe_board(b)
    b.print()


if __name__ == '__main__':
    main()
