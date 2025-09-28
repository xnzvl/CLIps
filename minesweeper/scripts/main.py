import sys

from src.clip import Runner
from src.game.sweeper import Minefield
from src.ui import BlessedTUI
from src.utils.configuration_parser import parse_sweeper_configuration


def main() -> None:
    configuration = parse_sweeper_configuration(sys.argv)

    sweeper = Minefield(configuration)
    ui = BlessedTUI(configuration.dimensions, configuration.mines)

    runner = Runner(sweeper, ui)
    runner.run()


if __name__ == '__main__':
    main()
