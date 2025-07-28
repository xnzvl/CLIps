import typing as t

import pyautogui as pag

Point = t.Tuple[int, int]
Dimensions = t.Tuple[int, int]
Color = t.Tuple[int, int, int]
Board = t.List[t.List['Tile']]
GameState = t.Tuple['GameProgress', Board]
Move = t.Tuple[Point, 'Click']

GameProgress = t.Literal['inProgress', 'victory', 'boom', 'notStarted']
Click = t.Literal['RMB', 'LMB']
Tile = t.Literal['_', '1', '2', '3', '4', '5', '6', '7', '8', '#', '!', '.', 'F']
"""
`Tile` represents a tile on a `Board`.
- numbers represent number of mines in the proximity of the `Tile`
- `_` symbolizes an empty `Tile`
- `#` stands for a `Tile` that was not uncovered yet
- `!` marks a `Tile` with a mine that has exploded
- `.` marks a `Tile` with a mine that hasn't exploded
- `F` symbolises a flag
"""

TILE_SIZE = 16

WHITE = 255, 255, 255
GRAY = 189, 189, 189
BLACK = 0, 0, 0
RED = 255, 0, 0

KEY_PIXEL_X_OFFSET = 9
KEY_PIXEL_Y_OFFSET = 10

SMILEY_WIDTH = 26

OFFSET_SMILEY_Y = -41
OFFSET_SMILEY_DEAD_X = 9
OFFSET_SMILEY_DEAD_Y = 9
OFFSET_SMILEY_SUNGLASSES_X = 9
OFFSET_SMILEY_SUNGLASSES_Y = 10

NUMBERS: t.Set[Tile] = {'1', '2', '3', '4', '5', '6', '7', '8'}

COLOR_TO_TILE: t.Dict[Color, Tile] = {
    GRAY: '_',
    (0, 0, 255): '1',
    (0, 123, 0): '2',
    (255, 0, 0): '3',
    (0, 0, 123): '4',
    (123, 0, 0): '5',
    (0, 123, 123): '6',
    (0, 0, 0): '7',
    (123, 123, 123): '8',
    (0, 0, 0): '.'
}


def is_number(tile: Tile) -> bool:
    return tile in NUMBERS


def print_game_state(game_state: GameState) -> None:
    progress, board = game_state

    print("Game progress:", progress)
    for row in board:
        print(' '.join(row))


def get_game_progress(top_left: Point, dimensions: Dimensions) -> GameProgress:
    x0, y0 = top_left
    width, _ = dimensions

    to_smiley_distance = (width * TILE_SIZE - SMILEY_WIDTH) // 2 - 1

    if pag.pixel(
            x0 + to_smiley_distance + OFFSET_SMILEY_DEAD_X,
            y0 + OFFSET_SMILEY_Y + OFFSET_SMILEY_DEAD_Y
    ) == BLACK:
        return 'boom'

    elif pag.pixel(
            x0 + to_smiley_distance + OFFSET_SMILEY_SUNGLASSES_X,
            y0 + OFFSET_SMILEY_Y + OFFSET_SMILEY_SUNGLASSES_Y
    ) == BLACK:
        return 'victory'

    return 'inProgress'


def get_game_board(top_left: Point, dimensions: Dimensions) -> Board:
    x0, y0 = top_left
    width, height = dimensions

    board: Board = list()

    for y1 in range(height):
        row: t.List[Tile] = list()

        for x1 in range(width):
            x = x0 + x1 * TILE_SIZE
            y = y0 + y1 * TILE_SIZE

            tile_color = pag.pixel(x, y)

            if tile_color == WHITE:
                row.append('#')
            elif tile_color == RED:
                row.append('!')
            else:
                tile = COLOR_TO_TILE.get(pag.pixel(x + KEY_PIXEL_X_OFFSET, y + KEY_PIXEL_Y_OFFSET))

                if tile is None:
                    raise ValueError('Invalid color')

                row.append(tile)

        board.append(row)

    return board


def get_game_state(top_left: Point, dimensions: Dimensions) -> GameState:
    return get_game_progress(top_left, dimensions), get_game_board(top_left, dimensions)


def count_uncovered_neighbours(board: Board, point: Point) -> int:
    x, y = point
    counter = 0

    for y_proximity in range():
        for x_proximity in range():
            if x_proximity == 0 and y_proximity == 0:
                continue

            if board[y][x] == '#' or board[y][x] == 'F':
                counter += 1

    return counter


def flag_neighbours(board: Board, point: Point) -> None:
    pass


def flag_mines(board: Board) -> None:
    """
      **Parameters:**
        - `Board` board
      ---
      **Description:**
        Modifies provided board - places flags on tiles that are 100% guaranteed to be a mine.
      ---
      **Returns:**
        `None`
    """
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if is_number(tile) and count_uncovered_neighbours(board, (x, y)) == int(tile):
                flag_neighbours(board, (x, y))


def recommend_move(board: Board) -> Move:
    flag_mines(board)


def play(top_left: Point, dimensions: Dimensions) -> None:
    game_progress, board = get_game_state(top_left, dimensions)

    while game_progress == 'inProgress':
        game_progress, board = get_game_state(top_left, dimensions)

        move = recommend_move(board)

        break

    if game_progress == 'boom':
        print('... oh no :[')
    else:
        print('victory!')


def main() -> None:
    play((251, 197), (9, 9))


if __name__ == '__main__':
    main()
