import sys

from src.clip.runner import Runner
from src.game.sweeper.impl.webpage_sweeper import WebPageSweeper
from src.ui.impl.blessed_tui import BlessedTUI
from src.utils.configuration_parser import parse_web_page_sweeper_configuration


def main() -> None:
    configuration = parse_web_page_sweeper_configuration(sys.argv)

    blessed_tui = BlessedTUI(configuration.dimensions, 0)
    sweeper = WebPageSweeper(configuration)

    runner = Runner(blessed_tui, sweeper)
    runner.go()


if __name__ == '__main__':
    main()
