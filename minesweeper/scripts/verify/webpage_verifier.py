import sys

import pyautogui as pag

from src.common import WebPageSweeperConfiguration
from src.game.sweeper import WebPageSweeper
from src.utils import parse_web_page_sweeper_configuration


def flag_corners(config: WebPageSweeperConfiguration) -> None:
    tile_size = WebPageSweeper.get_tile_size()

    width  = config.dimensions.width  * tile_size - 1
    height = config.dimensions.height * tile_size - 1

    pag.rightClick(
        config.offsets.x,
        config.offsets.y
    )
    pag.rightClick(
        config.offsets.x + width,
        config.offsets.y
    )
    pag.rightClick(
        config.offsets.x + width,
        config.offsets.y + height
    )
    pag.rightClick(
        config.offsets.x,
        config.offsets.y + height
    )


def main() -> None:
    config = parse_web_page_sweeper_configuration(sys.argv)
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
