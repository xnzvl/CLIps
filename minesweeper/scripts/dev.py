import sys

from src.clip.runner import Runner
from src.game.sweeper import WebPageSweeper
from src.ui import BlessedTUI
from src.utils import parse_web_page_sweeper_configuration


def main() -> None:
    config = parse_web_page_sweeper_configuration(sys.argv)

    sweeper = WebPageSweeper(config)
    ui = BlessedTUI(config.dimensions, config.mines)

    runner = Runner(sweeper, ui)
    runner.go()


if __name__ == '__main__':
    main()
