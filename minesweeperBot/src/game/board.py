from typing import Dict, Callable, List

from src.common import BoardObservation, TileObservation, NUMBER_TILE_OBSERVATION
from src.game.tile import Tile


class Board:
    _observationToAction: Dict[TileObservation, Callable[[Tile], None]] = {
        '*': lambda t: t.place_mine(True),
        '+': lambda t: t.place_mine(False),
        'F': lambda t: t.place_flag(),
        'O': lambda t: t.set_covered(),
        ' ': lambda t: t.set_empty()
    }

    def __init__(self, width: int, height: int) -> None:
        if width < 1:
            raise ValueError(f'width has to be greater than 1 (provided {width})')
        if height < 1:
            raise ValueError(f'height has to be greater than 1 (provided {height})')

        self._width = width
        self._height = height
        self._tiles: List[List[Tile]] = [
            [Tile() for _ in range(width)]
            for _ in range(height)
        ]

    def _validate_position(self, x: int, y: int) -> None:
        if x < 0:
            raise ValueError('x cannot be lower than 0')
        if x >= self._width:
            raise ValueError(f'x cannot be greater than width of the board ({self._width})')

        if y < 0:
            raise ValueError('y cannot be lower than 0')
        if y >= self._height:
            raise ValueError(f'y cannot be greater than height of the board ({self._height})')

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_tiles(self) -> List[List[Tile]]:
        return self._tiles

    def get_tile_at(self, x: int, y: int) -> Tile:
        self._validate_position(x, y)
        return self._tiles[y][x]

    def get_neighbours_of_tile_at(self, x: int, y: int) -> List[Tile]:
        self._validate_position(x, y)
        neighbours: List[Tile] = list()

        for y_proximity in range(-1 if y != 0 else 0, 2 if y != self._height - 1 else 1):
            for x_proximity in range(-1 if x != 0 else 0, 2 if x != self._width - 1 else 1):
                if x_proximity == 0 and y_proximity == 0:
                    continue

                neighbours.append(self._tiles[y + y_proximity][x + x_proximity])

        return neighbours

    def update(self, observation: BoardObservation) -> None:
        if len(self._tiles) != len(observation):
            raise ValueError('height of boards isn\'t equal')
        if len(self._tiles[0]) != len(observation[0]):
            raise ValueError('width of boards isn\'t equal')

        for y, row in enumerate(self._tiles):
            for x, tileObservation in enumerate(row):
                observed = observation[y][x]
                if observed in NUMBER_TILE_OBSERVATION:
                    tileObservation.set_count(int(observed))
                else:
                    self._observationToAction[observed](tileObservation)

    def is_valid(self) -> bool:
        # TODO
        return False
