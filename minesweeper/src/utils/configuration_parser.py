from argparse import ArgumentParser
from typing import List

from src.common import Configuration, Dimensions, Point, SweeperConfiguration, WebPageSweeperConfiguration, DEFAULT_USERNAME


def _init_core_parser() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        '-width',
        metavar='WIDTH',
        type=int,
        help='minefield width measured in tiles',
        required=True
    )
    parser.add_argument(
        '-height',
        metavar='HEIGHT',
        type=int,
        help='minefield height measured in tiles',
        required=True
    )
    parser.add_argument(
        '-mines',
        metavar='MINES',
        type=int,
        help='number of mines',
        required=True
    )

    parser.add_argument(
        '-qm', '--question_marks',
        metavar='QUESTION_MARKS',
        type=bool,
        help='flag to signal whether question marks are enabled or not',
        default=False
    )
    parser.add_argument(
        '-u', '--username',
        metavar='USERNAME',
        type=str,
        help='username to be used',
        default=DEFAULT_USERNAME
    )

    return parser


SWEEPER_CONFIGURATION_CORE_PARSER = _init_core_parser()


def parse_configuration(argv: List[str]) -> Configuration[SweeperConfiguration]:
    parser = ArgumentParser(
        prog=argv[0],  # TODO: adjust
        parents=[SWEEPER_CONFIGURATION_CORE_PARSER]
    )

    ns = parser.parse_args(argv[1:])

    return Configuration(
        sweeper_configuration=SweeperConfiguration(
            dimensions=Dimensions(ns.width, ns.height),
            mines=ns.mines,
            question_marks=ns.question_marks
        ),
        username=ns.username
    )


def parse_web_page_configuration(argv: List[str]) -> Configuration[WebPageSweeperConfiguration]:
    parser = ArgumentParser(
        prog=argv[0],  # TODO: adjust
        parents=[SWEEPER_CONFIGURATION_CORE_PARSER]
    )

    parser.add_argument(
        '-x_offset',
        metavar='X_OFFSET',
        type=int,
        help='X offset',
        required=True
    )
    parser.add_argument(
        '-y_offset',
        metavar='Y_OFFSET',
        type=int,
        help='Y offset',
        required=True
    )

    ns = parser.parse_args(argv[1:])

    return Configuration(
        sweeper_configuration=WebPageSweeperConfiguration(
            dimensions=Dimensions(ns.width, ns.height),
            mines=ns.mines,
            question_marks=ns.question_marks,
            offsets=Point(ns.x_offset, ns.y_offset)
        ),
        username=ns.username
    )
