from multiprocessing.managers import SharedMemoryManager


class SharableListChunk:
    def __init__(self, list_size: int) -> None:
        self._smm = SharedMemoryManager()
        self._smm.start()

        self.victories = self._smm.ShareableList(
            [ 0 for _ in range(list_size) ]
        )
        self.errors = self._smm.ShareableList(
            [ False for _ in range(list_size) ]
        )

    def dispose(self) -> None:
        self._smm.shutdown()
        self._smm.join()
