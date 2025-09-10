from src.common import WebPageSweeperConfiguration
from src.game.impl.webpage_sweeper import WebPageSweeper
from src.solving.bot.bot import Bot
from src.solving.strategy.strategy import Strategy


def new_web_page_bot(
        configuration: WebPageSweeperConfiguration,
        strategy: Strategy,
        with_question_marks: bool
) -> Bot:
    return Bot(
        WebPageSweeper(configuration, with_question_marks),
        strategy
    )
