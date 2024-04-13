import time
import typing


# =============================================================================
#  CUSTOM TYPES


Tower = typing.List[int]
Board = typing.Tuple[Tower, Tower, Tower]
TowerIndex = typing.Literal[0, 1, 2]


# =============================================================================
#  CONSTANTS


DISC_COUNT = MAX_DISC_RADIUS = 9
BLOCK_CHAR = "█"
GROUND_CHAR = "_"


# =============================================================================
#  PRINTING


def get_layer_str(
        board: Board,
        tower_index: TowerIndex,
        layer: int
) -> str:
    disc_radius = 0 \
        if len(board[tower_index]) < layer \
        else board[tower_index][layer - 1]

    blank_char = " " if layer != 1 else GROUND_CHAR

    return blank_char * (MAX_DISC_RADIUS - disc_radius) \
        + BLOCK_CHAR * disc_radius \
        + ("|" if disc_radius == 0 else BLOCK_CHAR) \
        + BLOCK_CHAR * disc_radius \
        + blank_char * (MAX_DISC_RADIUS - disc_radius)


def print_board(
        board: Board
) -> None:
    for layer in range(DISC_COUNT + 1, 0, -1):
        separator = " " if layer != 1 else GROUND_CHAR

        print(
            separator + get_layer_str(board, 0, layer)
            + separator + get_layer_str(board, 1, layer)
            + separator + get_layer_str(board, 2, layer)
            + separator
        )


# =============================================================================
#  CORE


def get_free_index(
        src_index: TowerIndex,
        dst_index: TowerIndex
) -> TowerIndex:
    return typing.cast(TowerIndex, 3 - (src_index + dst_index))


def move_disc(
        board: Board,
        src_index: TowerIndex,
        dst_index: TowerIndex
) -> None:
    board[dst_index].append(board[src_index].pop())

    print_board(board)
    time.sleep(0.1)


def move_disc_range(
        board: Board,
        src_index: TowerIndex,
        dst_index: TowerIndex,
        range: int
) -> None:
    if range == 1:
        move_disc(board, src_index, dst_index)
        return

    free_index = get_free_index(src_index, dst_index)

    move_disc_range(board, src_index, free_index, range - 1)
    move_disc(board, src_index, dst_index)
    move_disc_range(board, free_index, dst_index, range - 1)


def move_tower(
        board: Board,
        src_index: TowerIndex,
        dst_index: TowerIndex
) -> None:
    move_disc_range(board, src_index, dst_index, len(board[src_index]))


# =============================================================================
#  RUNNING


def main() -> int:
    a = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    b: typing.List[int] = list()
    c: typing.List[int] = list()
    board = (a, b, c)

    move_tower(board, 0, 2)

    return 0


if __name__ == "__main__":
    main()
