from threading import Timer
from typing import Callable


class Repeater:
    def __init__[**P, R](
            self,
            interval: float,
            function: Callable[P, R],
            *args: P.args,
            **kwargs: P.kwargs
    ) -> None:
        self._interval = interval
        self._function = function
        self._args = args
        self._kwargs = kwargs

        self._timer: Timer | None = None
        self._is_running = False

    def _repeat(self) -> None:
        self._function(*self._args, **self._kwargs)

        self._timer = Timer(self._interval, self._repeat)
        self._timer.start()

    def start(self) -> None:
        if not self._is_running:
            self._is_running = True
            self._repeat()

    def stop(self) -> None:
        if self._is_running:
            assert self._timer is not None

            self._timer.cancel()
            self._timer = None

            self._is_running = False

    @property
    def is_running(self) -> bool:
        return self._is_running
