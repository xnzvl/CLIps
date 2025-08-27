from src.solving.bot.generic_bot import GenericBot

from src.common import Configuration
from src.mediator.impl.webpage_mediator import WebPageMediator
from src.solving.strategy.strategy import Strategy


class WebPageBot(GenericBot):
    def __init__(self, configuration: Configuration, strategy: Strategy, with_question_marks: bool) -> None:
        super().__init__(
            configuration,
            strategy,
            lambda c: WebPageMediator(c, with_question_marks)
        )
