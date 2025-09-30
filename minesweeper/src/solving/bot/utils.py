from math import log10
from typing import List, Callable

from src.game.sweeper import Result


def get_printing_result_consumer(solve_attempts: int, accumulator: List[Result] | None = None) -> Callable[[int, Result], None]:
    max_digits = int(log10(solve_attempts)) + 1

    def consumer(attempt_number: int, result: Result) -> None:
        print(f'Attempt #{attempt_number:0{max_digits}}: {result}')

        if accumulator is not None:
            accumulator.append(result)

    return consumer


def print_winrate(attempts: int, victories: int) -> None:
    print(f'Achieved {victories} victories from {attempts} attempts')
    print(f'  => winrate: {victories / attempts * 100:.3f}%')
