import sys

from src.clip.runner import Runner
from src.game.sweeper import WebPageSweeper
from src.ui import BlessedTUI
from src.utils import parse_web_page_configuration


def main() -> None:
    configuration = parse_web_page_configuration(sys.argv)
    sweeper_configuration = configuration.sweeper_configuration

    sweeper = WebPageSweeper(sweeper_configuration)
    ui = BlessedTUI(sweeper_configuration.dimensions, configuration.username)

    runner = Runner(sweeper, ui)
    runner.run()


if __name__ == '__main__':
    main()
