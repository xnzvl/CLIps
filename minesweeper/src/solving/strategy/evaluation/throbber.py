class Throbber:
    def __init__(self) -> None:
        self._index = 0
        self._stages = ['⠏', '⠛', '⠹', '⠼', '⠶', '⠧']

    def get_and_increment(self) -> str:
        char = self._stages[self._index]
        self._index = (self._index + 1) % len(self._stages)

        return char
