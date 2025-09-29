from typing import Literal, overload

from .minesweeper_error import MinesweeperError


class AttemptError(MinesweeperError):
    ...


# TODO: use on more places instead of tuple with Nones
class Attempt[R, E]:
    """
    Class that represents an attempt of something.
    It can either result in success or failure.

    V: result type
    E: error type
    """

    @staticmethod
    def success(result: R) -> 'Attempt[R, E]':
        """
        Create a successful Attempt instance.

        :param result: Attempt result
        :returns:      successful Attempt
        """
        return Attempt[R, E](True, result, None)

    @staticmethod
    def failure(error: E) -> 'Attempt[R, E]':
        """
        Create a failed Attempt instance.

        Parameters
        ---
        error : Y
            Attempt error

        Returns
        ---
        Attempt[X, Y]
            failed Attempt
        """
        return Attempt[R, E](False, None, error)

    @overload
    def __init__(self, is_successful: Literal[True], result: R, error: Literal[None]) -> None:
        ...

    @overload
    def __init__(self, is_successful: Literal[False], result: Literal[None], error: E) -> None:
        ...

    def __init__(self, is_successful: bool, result: R | None, error: E | None) -> None:
        """
        Create an instance.

        Parameters
        ---
        is_successful : bool
            whether the attempt was successful
        result : X
            result of the successful attempt
        error : Y
            error of the failed attempt

        Returns
        ---
        Attempt[X, Y]
            Attempt instance
        """

        if is_successful:
            assert result is not None and error is None
        else:
            assert result is None     and error is not None

        self._is_success = is_successful
        self._result = result
        self._error = error

    @property
    def is_successful(self) -> bool:
        """
        Flag whether the attempt was successful.
        """
        return self._is_success

    @property
    def result(self) -> R:
        """
        Result of the successful attempt.

        Raises
        ---
        AttemptError
            if Attempt is not successful

        Returns
        ---
        X
            Attempt result
        """
        if self._result is None:
            raise AttemptError('attempt failed -> no result')

        return self._result

    @property
    def error(self) -> E:
        """
        Error of the failed attempt.

        Raises
        ---
        AttemptError
            if Attempt is successful

        Returns
        ---
        Y
            Attempt error
        """
        if self._error is None:
            raise AttemptError('attempt succeeded -> no error')

        return self._error
