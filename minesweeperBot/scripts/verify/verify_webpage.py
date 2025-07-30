import sys

import pyautogui as pag

from src.common import Configuration
from src.mediators.impl.webpage_mediator import TILE_SIZE
from utils.configuration_parser import parse_configuration


def flag_corners(config: Configuration) -> None:
    pag.rightClick(
        config.offsets.x,
        config.offsets.y
    )
    pag.rightClick(
        config.offsets.x + config.dimensions.width * TILE_SIZE - 1,
        config.offsets.y
    )
    pag.rightClick(
        config.offsets.x + config.dimensions.width * TILE_SIZE - 1,
        config.offsets.y + config.dimensions.height * TILE_SIZE - 1
    )
    pag.rightClick(
        config.offsets.x,
        config.offsets.y + config.dimensions.height * TILE_SIZE - 1
    )


def main() -> None:
    config = parse_configuration(sys.argv)
    flag_corners(config)

    print()
    print('==== PROVIDED CONFIGURATION ====')
    print('  offsets:')
    print(f'    x = {config.offsets.x}')
    print(f'    y = {config.offsets.y}')
    print('  dimensions:')
    print(f'    width = {config.dimensions.width}')
    print(f'    height = {config.dimensions.height}')
    print()
    print('If you don\'t see flags in all four corners then the provided configuration is wrong.')
    print()


if __name__ == '__main__':
    main()
