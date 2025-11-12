import sys

from src.clip import Runner
from src.game.sweeper import Minefield
from src.ui import BlessedTUI
from src.utils.configuration_parser import parse_configuration


def main() -> None:
    configuration = parse_configuration(sys.argv)
    sweeper_configuration = configuration.sweeper_configuration

    sweeper = Minefield(sweeper_configuration)
    ui = BlessedTUI(sweeper_configuration.dimensions, configuration.username)

    runner = Runner(sweeper, ui)
    runner.run()


if __name__ == '__main__':
    main()
