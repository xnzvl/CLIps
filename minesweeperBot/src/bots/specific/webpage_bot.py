from src.bots.bot import Bot

from src.common import Configuration
from src.mediators.impl.webpage_mediator import WebPageMediator
from src.strategies.strategy import Strategy


class WebPageBot(Bot):
    def __init__(self, configuration: Configuration, strategy: Strategy):
        super().__init__(
            configuration,
            strategy,
            lambda c: WebPageMediator(c)
        )
