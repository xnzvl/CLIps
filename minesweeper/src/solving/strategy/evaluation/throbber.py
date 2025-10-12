class Throbber:
    _stages = ['⠏', '⠛', '⠹', '⠼', '⠶', '⠧']

    def __init__(self, progress_stages: int = 1) -> None:
        self._index = 0
        self._progress = 0

        self._progress_stages = progress_stages

    def get_and_progress(self) -> str:
        char = Throbber._stages[self._index]

        self._progress += 1
        if self._progress == self._progress_stages:
            self._index = (self._index + 1) % len(Throbber._stages)
            self._progress = 0

        return char
