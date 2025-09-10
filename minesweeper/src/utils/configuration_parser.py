from argparse import ArgumentParser
from typing import List

from src.common import WebPageSweeperConfiguration, Dimensions, Point, SweeperConfiguration


def _add_core_arguments(parser: ArgumentParser) -> None:
    parser.add_argument('width', metavar='WIDTH', type=int, help='width')
    parser.add_argument('height', metavar='HEIGHT', type=int, help='height')
    parser.add_argument('mines', metavar='MINES', type=int, help='number of mines')


def parse_configuration(argv: List[str]) -> SweeperConfiguration:
    parser = ArgumentParser(prog=argv[0])

    _add_core_arguments(parser)
    ns = parser.parse_args(argv[1:])

    return SweeperConfiguration(
        dimensions=Dimensions(ns.width, ns.height),
        mines=ns.mines
    )


def parse_web_page_configuration(argv: List[str]) -> WebPageSweeperConfiguration:
    parser = ArgumentParser(prog=argv[0])

    parser.add_argument('x_offset', metavar='X_OFFSET', type=int, help='X offset')
    parser.add_argument('y_offset', metavar='Y_OFFSET', type=int, help='Y offset')

    _add_core_arguments(parser)
    ns = parser.parse_args(argv[1:])

    return WebPageSweeperConfiguration(
        dimensions=Dimensions(ns.width, ns.height),
        mines=ns.mines,
        offsets=Point(ns.x_offset, ns.y_offset)
    )
