from multiprocessing import Pipe, reduction
from multiprocessing.connection import Connection, PipeConnection
from typing import Callable, Literal, Tuple, cast, overload


class _ConnectionWrapper:
    @staticmethod
    def reduction[T: _ConnectionWrapper](
            wrapper: T
    ) -> Tuple[Callable[[Connection | PipeConnection], T], Tuple[Connection | PipeConnection]]:
        return (
            wrapper.__class__,
            (wrapper._connection,)
        )

    def __init__(self, connection: Connection | PipeConnection) -> None:
        self._connection = connection

    def close(self) -> None:
        self._connection.close()


class SenderPipe[T](_ConnectionWrapper):
    def __init__(self, connection: Connection | PipeConnection) -> None:
        super().__init__(connection)

    def send(self, obj: T) -> None:
        self._connection.send(obj)


class ReceiverPipe[T](_ConnectionWrapper):
    def __init__(self, connection: Connection | PipeConnection) -> None:
        super().__init__(connection)

    def recv(self) -> T:
        return cast(T, self._connection.recv())


class DuplexPipe[T](SenderPipe[T], ReceiverPipe[T]):
    def __init__(self, connection: Connection | PipeConnection) -> None:
        super().__init__(connection)


class PipeFactory[T]:
    @staticmethod
    @overload
    def create(duplex: Literal[False]) -> Tuple[ReceiverPipe[T], SenderPipe[T]]:
        ...

    @staticmethod
    @overload
    def create(duplex: Literal[True] = True) -> Tuple[DuplexPipe[T], DuplexPipe[T]]:
        ...

    @staticmethod
    def create(duplex: bool = True) -> Tuple[DuplexPipe[T], DuplexPipe[T]] | Tuple[ReceiverPipe[T], SenderPipe[T]]:
        conn1, conn2 = Pipe(duplex)

        return (DuplexPipe[T](conn1), DuplexPipe[T](conn2)) \
            if duplex \
            else (ReceiverPipe[T](conn1), SenderPipe[T](conn2))

    def __init__(self) -> None:
        raise NotImplementedError('not meant to be instantiated')


reduction.register(DuplexPipe, _ConnectionWrapper.reduction)
reduction.register(ReceiverPipe, _ConnectionWrapper.reduction)
reduction.register(SenderPipe, _ConnectionWrapper.reduction)
