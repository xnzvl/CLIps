# TODO: move to related packages

class InvalidStateError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class FrozenInstanceError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
