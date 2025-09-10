from src.game.impl.webpage_sweeper import WebPageSweeper
from src.solving.bot.generic_bot import GenericBot

from src.common import WebPageSweeperConfiguration
from src.solving.strategy.strategy import Strategy


class WebPageBot(GenericBot):  # TODO: scrap this and create BotFactory
    def __init__(self, configuration: WebPageSweeperConfiguration, strategy: Strategy, with_question_marks: bool) -> None:
        super().__init__(
            configuration,
            strategy,
            lambda c: WebPageSweeper(c, with_question_marks)
        )
