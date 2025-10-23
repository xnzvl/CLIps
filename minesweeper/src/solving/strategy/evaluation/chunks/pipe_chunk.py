from typing import Literal

from ..typed_pipe import PipeFactory
from ..types import RecordPosition, RecordUpdate


class PipeChunk:
    def __init__(self) -> None:
        self.progress_updates_receiver, self.progress_updates_sender = \
            PipeFactory[RecordUpdate | None].create(False)

        self.throbber_updates_receiver, self.throbber_updates_sender = \
            PipeFactory[RecordPosition | None].create(False)

        self.throbber_ack_receiver,     self.throbber_ack_sender     = \
            PipeFactory[Literal[None]].create(False)

    def dispose(self) -> None:
        self.progress_updates_receiver.close()
        self.progress_updates_sender.close()

        self.throbber_updates_receiver.close()
        self.throbber_updates_sender.close()

        self.throbber_ack_receiver.close()
        self.throbber_ack_sender.close()
