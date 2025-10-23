class Throbber:
    _stages = ['⠏', '⠛', '⠹', '⠼', '⠶', '⠧']

    def __init__(self) -> None:
        self._index = 0

    def get_and_progress(self) -> str:
        char = Throbber._stages[self._index]

        self._index = (self._index + 1) % len(Throbber._stages)

        return char
