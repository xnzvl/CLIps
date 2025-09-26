# TODO: use on more places instead of tuple with Nones
class Attempt[X, Y]:
    @staticmethod
    def success(value: X) -> 'Attempt[X, Y]':
        return Attempt[X, Y](True, value, None)

    @staticmethod
    def failure(error: Y) -> 'Attempt[X, Y]':
        return Attempt[X, Y](False, None, error)

    def __init__(self, is_success: bool, value: X | None, error: Y | None) -> None:
        if is_success:
            assert value is not None and error is None
        else:
            assert value is None     and error is not None

        self._is_success = is_success
        self._value = value
        self._error = error

    @property
    def is_successful(self) -> bool:
        return self._is_success

    @property
    def value(self) -> X:
        return self._value

    @property
    def error(self) -> Y:
        return self._error
