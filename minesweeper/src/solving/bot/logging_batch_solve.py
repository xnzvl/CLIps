from functools import partial
from math import log10

from blessed import Terminal

from src.game.sweeper import GameState, Result

from .bot import Bot


TERMINAL = Terminal()


def write_attempt(digits: int, attempt_number: int, result: str) -> None:
    print(f'    #{attempt_number+1:0{digits}} {result}')


def exception_consumer(digits: int, i: int, exception: Exception) -> None:
    write_attempt(digits, i, f'{TERMINAL.darkorchid('ERROR!')} {TERMINAL.darkorchid4(str(exception))}')


def result_consumer(digits: int, i: int, result: Result) -> None:
    formatter = TERMINAL.bright_green if result == GameState.VICTORY else TERMINAL.firebrick1

    write_attempt(digits, i, f'{formatter(result.value.capitalize())}')


def logging_batch_solve(bot: Bot, batch_size: int) -> None:
    if batch_size == 0:
        raise ValueError('batch size must be greater than 0')

    print()
    print(f'  {TERMINAL.bright_white(f'Batch size: {batch_size}')}')
    # TODO: more details
    # TODO: needs more getters from Bot

    digits = int(log10(batch_size)) + 1
    bot.batch_solve(
        batch_size,
        partial(result_consumer, digits),
        partial(exception_consumer, digits)
    )

    print()
