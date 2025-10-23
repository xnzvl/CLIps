from multiprocessing import Pipe


class PipeChunk:
    def __init__(self) -> None:
        self.progress_updates_receiver, self.progress_updates_sender = Pipe(False)
        self.throbber_updates_receiver, self.throbber_updates_sender = Pipe(False)
        self.throbber_ack_receiver,     self.throbber_ack_sender     = Pipe(False)

    def dispose(self) -> None:
        self.progress_updates_receiver.close()
        self.progress_updates_sender.close()

        self.throbber_updates_receiver.close()
        self.throbber_updates_sender.close()

        self.throbber_ack_receiver.close()
        self.throbber_ack_sender.close()
