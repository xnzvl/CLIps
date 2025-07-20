import sys

from src.interactions.webpage.webpage_observer import WebPageObserver
from utils.configuration_parser import parse_configuration


def main() -> None:
    configuration = parse_configuration(sys.argv)

    observer = WebPageObserver(configuration)
    game_state = observer.observe_state()

    print(game_state)


if __name__ == '__main__':
    main()
