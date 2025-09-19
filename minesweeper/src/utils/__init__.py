# TODO: __all__

# TODO: actually use? instead of tuple with Nones
#       move to separate file
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

        self.is_success = is_success
        self.value = value
        self.error = error
