from dataclasses import dataclass
from functools import partial
from math import log10

from blessed import Terminal

from src.game.sweeper import GameState, Result

from .bot import Bot


TERMINAL = Terminal()


@dataclass
class Results:
    failures:   int = 0
    exceptions: int = 0


def write_attempt(digits: int, attempt_number: int, result: str) -> None:
    print(f'    #{attempt_number+1:0{digits}} {result}')


def exception_consumer(results: Results, digits: int, i: int, exception: Exception) -> None:
    results.exceptions += 1
    write_attempt(digits, i, f'{TERMINAL.darkorchid('ERROR!')} {TERMINAL.darkorchid4(str(exception))}')

def result_consumer(results: Results, digits: int, i: int, result: Result) -> None:
    is_victory = result == GameState.VICTORY
    results.failures += 0 if is_victory else 1
    formatter = TERMINAL.bright_green if is_victory else TERMINAL.firebrick1
    write_attempt(digits, i, f'{formatter(result.value.capitalize())}')


def logging_batch_solve(bot: Bot, batch_size: int) -> None:
    if batch_size == 0:
        raise ValueError('batch size must be greater than 0')

    print()
    print(f'  {TERMINAL.bright_white(f'Batch size: {batch_size}')}')
    # TODO: more details
    # TODO: needs more getters from Bot

    digits = int(log10(batch_size)) + 1
    results = Results()
    victories = bot.batch_solve(
        batch_size,
        partial(result_consumer, results, digits),
        partial(exception_consumer, results, digits)
    )

    print()
    print(f'  {TERMINAL.bright_white(f'Victories:  {victories          / batch_size * 100:.3f}%')}')
    print(f'  {TERMINAL.bright_white(f'Failures:   {results.failures   / batch_size * 100:.3f}%')}')
    print(f'  {TERMINAL.bright_white(f'Exceptions: {results.exceptions / batch_size * 100:.3f}%')}')
    print()
    print(f'  {TERMINAL.bright_white(f'Winrate: {victories / (batch_size - results.exceptions) * 100:.3f}%')}')
    print()
