from src.game.impl.webpage_sweeper import WebPageSweeper
from src.solving.bot.generic_bot import GenericBot

from src.common import Configuration
from src.solving.strategy.strategy import Strategy


class WebPageBot(GenericBot):
    def __init__(self, configuration: Configuration, strategy: Strategy, with_question_marks: bool) -> None:
        super().__init__(
            configuration,
            strategy,
            lambda c: WebPageSweeper(c, with_question_marks)
        )
