import typing

Tower = typing.List[int]
Board = typing.Tuple[Tower, Tower, Tower]
Slot = typing.Literal[0, 1, 2]


def get_free_slot(
        src_slot: Slot,
        dst_slot: Slot
) -> Slot:
    return typing.cast(Slot, 3 - (src_slot +  dst_slot))


def move_disc(
        board: Board,
        src_slot: Slot,
        dst_slot: Slot
) -> None:
    board[dst_slot].append(board[src_slot].pop())

    a, b, c = board
    print("a: ", a)
    print("b: ", b)
    print("c: ", c)
    print()


def move_disc_range(
        board: Board,
        src_slot: Slot,
        dst_slot: Slot,
        range: int
) -> None:
    if range == 1:
        move_disc(board, src_slot, dst_slot)
        return
    
    free_slot = get_free_slot(src_slot, dst_slot)

    move_disc_range(board, src_slot, free_slot, range - 1)
    move_disc(board, src_slot, dst_slot)
    move_disc_range(board, free_slot, dst_slot, range - 1)


def move_tower(
        board: Board,
        src_slot: Slot,
        dst_slot: Slot
) -> None:
    move_disc_range(board, src_slot, dst_slot, len(board[src_slot]))


def main() -> int:
    a = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    b: typing.List[int] = list()
    c: typing.List[int] = list()
    board = (a, b, c)

    move_tower(board, 0, 2)

    return 0


if __name__ == "__main__":
    main()
