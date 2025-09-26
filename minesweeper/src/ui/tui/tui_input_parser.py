from argparse import ArgumentParser
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from typing import cast

from src.common import Action, Point
from src.ui.input import Input
from src.utils import Attempt


def create_input_parser(is_game_in_progress: bool) -> ArgumentParser:
    # TODO: I personally don't like creating the parser each time
    #       but I doubt it's *that* performance heavy
    #       ANYWAYS!
    #       I'd love to have two separate *constant* parsers
    #       but for now I'll follow D. E. Knuth's advice

    parser = ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    if is_game_in_progress:
        point_parser = ArgumentParser(add_help=False)
        point_parser.add_argument('x', type=int)
        point_parser.add_argument('y', type=int)

        uncover_parser  = subparsers.add_parser('uncover',  aliases=['u'],  parents=[point_parser])
        uncover_parser .set_defaults(action=Action.UNCOVER)

        flag_parser     = subparsers.add_parser('flag',     aliases=['f'],  parents=[point_parser])
        flag_parser    .set_defaults(action=Action.FLAG)

        question_parser = subparsers.add_parser('question', aliases=['qm'], parents=[point_parser])
        question_parser.set_defaults(action=Action.QUESTION_MARK)

        clear_parser    = subparsers.add_parser('clear',    aliases=['c'],  parents=[point_parser])
        clear_parser   .set_defaults(action=Action.CLEAR)

    reset_parser = subparsers.add_parser('reset', aliases=['r'])
    reset_parser.set_defaults(action=Action.RESET)

    quit_parser  = subparsers.add_parser('quit',  aliases=['q'])
    quit_parser .set_defaults(action=Action.QUIT)

    return parser


def obtain_input(is_game_in_progress: bool) -> Attempt[Input, str]:
    try:
        input_string = input()
    except KeyboardInterrupt:
        return Attempt.success(Input(Action.QUIT))

    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        try:
            ns = create_input_parser(is_game_in_progress) \
                .parse_args(input_string.split())
        except SystemExit:
            return Attempt.failure(input_string)

    action = cast(Action, ns.action)
    if action == Action.RESET or action == Action.QUIT:
        return Attempt.success(Input(action))

    x, y = cast(int, ns.x), cast(int, ns.y)
    return Attempt.success(Input(action, Point(x, y)))
