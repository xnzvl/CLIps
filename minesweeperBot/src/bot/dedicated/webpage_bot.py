from src.bot.generic_bot import GenericBot

from src.common import Configuration
from src.mediator.impl.webpage_mediator import WebPageMediator
from src.strategy.strategy import Strategy


class WebPageBot(GenericBot):
    def __init__(self, configuration: Configuration, strategy: Strategy):
        super().__init__(
            configuration,
            strategy,
            lambda c: WebPageMediator(c)
        )
