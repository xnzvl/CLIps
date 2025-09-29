from src.common import WebPageSweeperConfiguration
from src.game.sweeper.impl.webpage_sweeper import WebPageSweeper
from src.solving.bot.bot import Bot
from src.solving.strategy.strategy import Strategy


class BotFactory:
    @staticmethod
    def get_webpage_bot(configuration: WebPageSweeperConfiguration, strategy: Strategy, username: str) -> Bot:
        return Bot(
            WebPageSweeper(configuration),
            strategy,
            username
        )
