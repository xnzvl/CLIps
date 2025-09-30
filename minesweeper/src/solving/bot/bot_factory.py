from src.common import SweeperConfiguration, WebPageSweeperConfiguration
from src.game.sweeper import Minefield, WebPageSweeper
from src.solving.bot import Bot
from src.solving.strategy import Strategy


class BotFactory:
    @staticmethod
    def get_webpage_bot(configuration: WebPageSweeperConfiguration, strategy: Strategy, username: str) -> Bot:
        return Bot(
            WebPageSweeper(configuration),
            strategy,
            username
        )

    @staticmethod
    def get_minefield_bot(configuration: SweeperConfiguration, strategy: Strategy, username: str) -> Bot:
        return Bot(
            Minefield(configuration),
            strategy,
            username
        )
