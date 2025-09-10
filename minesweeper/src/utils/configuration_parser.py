from argparse import ArgumentParser
from typing import List

from src.common import WebPageSweeperConfiguration, Dimensions, Point, SweeperConfiguration

# TODO: refactor duplicate code


def parse_configuration(argv: List[str]) -> SweeperConfiguration:
    parser = ArgumentParser(prog=argv[0])

    parser.add_argument('width', metavar='WIDTH', type=int, help='width')
    parser.add_argument('height', metavar='HEIGHT', type=int, help='height')
    parser.add_argument('mines', metavar='MINES', type=int, help='number of mines')

    ns = parser.parse_args(argv[1:])

    return SweeperConfiguration(
        dimensions=Dimensions(ns.width, ns.height),
        mines=ns.mines
    )


def parse_web_page_configuration(argv: List[str]) -> WebPageSweeperConfiguration:
    parser = ArgumentParser(prog=argv[0])

    parser.add_argument('x_offset', metavar='X_OFFSET', type=int, help='X offset')
    parser.add_argument('y_offset', metavar='Y_OFFSET', type=int, help='Y offset')
    parser.add_argument('width', metavar='WIDTH', type=int, help='width')
    parser.add_argument('height', metavar='HEIGHT', type=int, help='height')
    parser.add_argument('mines', metavar='MINES', type=int, help='number of mines')

    ns = parser.parse_args(argv[1:])

    return WebPageSweeperConfiguration(
        dimensions=Dimensions(ns.width, ns.height),
        mines=ns.mines,
        offsets=Point(ns.x_offset, ns.y_offset)
    )
