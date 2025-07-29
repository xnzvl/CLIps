from src.bots.bot import Bot

from src.common import Configuration
from src.interactions.webpage.webpage_clicker import WebPageClicker
from src.interactions.webpage.webpage_observer import WebPageObserver
from src.strategies.strategy import Strategy


class WebPageBot(Bot):
    def __init__(self, configuration: Configuration, strategy: Strategy):
        super().__init__(
            configuration,
            strategy,
            lambda c: WebPageObserver(c),
            lambda c: WebPageClicker(c)
        )

    def _post_game_procedure(self) -> None:
        return
