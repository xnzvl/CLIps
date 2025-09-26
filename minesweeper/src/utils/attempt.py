from typing import Literal, overload


class AttemptError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


# TODO: use on more places instead of tuple with Nones
class Attempt[V, E]:
    """
    Class that represents an attempt of something.
    It can either result in success or failure.

    V: value type
    E: error type
    """

    @staticmethod
    def success(value: V) -> 'Attempt[V, E]':
        """
        Create a successful Attempt instance.

        :param value: Attempt value
        :returns:     successful Attempt
        """
        return Attempt[V, E](True, value, None)

    @staticmethod
    def failure(error: E) -> 'Attempt[V, E]':
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
        return Attempt[V, E](False, None, error)

    @overload
    def __init__(self, is_success: Literal[True], value: V, error: Literal[None]) -> None:
        ...

    @overload
    def __init__(self, is_success: Literal[False], value: Literal[None], error: E) -> None:
        ...

    def __init__(self, is_successful: bool, value: V | None, error: E | None) -> None:
        """
        Create an instance.

        Parameters
        ---
        is_successful : bool
            whether the attempt was successful
        value : X
            value of the successful attempt
        error : Y
            error of the failed attempt

        Returns
        ---
        Attempt[X, Y]
            Attempt instance
        """

        if is_successful:
            assert value is not None and error is None
        else:
            assert value is None     and error is not None

        self._is_success = is_successful
        self._value = value
        self._error = error

    @property
    def is_successful(self) -> bool:
        """
        Flag whether the attempt was successful.
        """
        return self._is_success

    @property
    def value(self) -> V:
        """
        Value of the successful attempt.

        Raises
        ---
        AttemptError
            if Attempt is not successful

        Returns
        ---
        X
            Attempt value
        """
        if self._value is None:
            raise AttemptError('attempt failed -> no value')

        return self._value

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
