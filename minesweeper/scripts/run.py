import sys

from src.utils.configuration_parser import parse_sweeper_configuration


def main() -> None:
    configuration = parse_sweeper_configuration(sys.argv)
    print(configuration)


if __name__ == '__main__':
    main()
