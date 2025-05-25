from argparse import ArgumentParser
from typing import List

from src.common import Configuration, Dimensions, Point


def parse_configuration(argv: List[str]) -> Configuration:
    parser = ArgumentParser(prog=argv[0])

    parser.add_argument('x_offset', metavar='X_OFFSET', type=int, help='X offset')
    parser.add_argument('y_offset', metavar='Y_OFFSET', type=int, help='Y offset')
    parser.add_argument('width', metavar='WIDTH', type=int, help='width')
    parser.add_argument('height', metavar='HEIGHT', type=int, help='height')
    parser.add_argument('-t', '--tile_size', type=int, help='tile_size', default=16)

    ns = parser.parse_args(argv[1:])

    return Configuration(
        offsets=Point(ns.x_offset, ns.y_offset),
        dimensions=Dimensions(ns.width, ns.height),
        tile_size=ns.tile_size
    )
