import sys

from src.utils.configuration_parser import parse_configuration


def main() -> None:
    configuration = parse_configuration(sys.argv)
    print(configuration)


if __name__ == '__main__':
    main()
