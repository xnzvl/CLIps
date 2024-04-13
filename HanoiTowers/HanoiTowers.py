import typing

Tower = typing.List[int]
Board = typing.Tuple[Tower, Tower, Tower]
TowerIndex = typing.Literal[0, 1, 2]


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


def main() -> int:
    a = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    b: typing.List[int] = list()
    c: typing.List[int] = list()
    board = (a, b, c)

    move_tower(board, 0, 2)

    return 0


if __name__ == "__main__":
    main()
