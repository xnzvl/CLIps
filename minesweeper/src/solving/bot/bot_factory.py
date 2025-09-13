from src.common import WebPageSweeperConfiguration
from src.game.sweeper.impl.webpage_sweeper import WebPageSweeper
from src.solving.bot.bot import Bot
from src.solving.strategy.strategy import Strategy


def new_web_page_bot(
        configuration: WebPageSweeperConfiguration,
        strategy: Strategy
) -> Bot:
    return Bot(
        WebPageSweeper(configuration),
        strategy
    )
