from multiprocessing.connection import Connection, Pipe, PipeConnection
from typing import Literal, Tuple, cast, overload


# TODO: make it work


class _Pipe:
    def __init__(self, connection: Connection | PipeConnection) -> None:
        self._connection = connection

    def close(self) -> None:
        self._connection.close()


class SenderPipe[T](_Pipe):
    def __init__(self, connection: Connection | PipeConnection) -> None:
        super().__init__(connection)

    def send(self, obj: T) -> None:
        self._connection.send(obj)


class ReceiverPipe[T](_Pipe):
    def __init__(self, connection: Connection | PipeConnection) -> None:
        super().__init__(connection)

    def recv(self) -> T:
        return cast(T, self._connection.recv())


class DuplexPipe[T](SenderPipe[T], ReceiverPipe[T]):
    def __init__(self, connection: Connection | PipeConnection) -> None:
        super().__init__(connection)


class GenericPipe[T]:
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
            else (ReceiverPipe[T](conn2), SenderPipe[T](conn1))
