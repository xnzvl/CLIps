from typing import Any, List, Literal, Set, Tuple

Value = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]
Cell = Value | None


class Sudoku:
    def __init__(self):
        self._grid: List[List[Cell]] = [[None for _ in range(9)] for _ in range(9)]

    def __getitem__(self, key: Tuple[int, int]) -> Cell:
        x, y = key

        # TODO: clean up
        if x < 0 or y < 0 or x >= 9 or y >= 9:
            raise IndexError("Index out of range")

        return self._grid[y][x]

    def _is_subsquare_valid(
            self,
            row_values: List[Set[Value]],
            column_values: List[Set[Value]],
            subsquare_x: int,
            subsquare_y: int
    ) -> bool:
        for add_y in range(3):
            for add_x in range(3):
                pass

    # TODO: implement caching version?
    #       it would check only relevant subsquares, rows and columns
    def is_valid(self) -> bool:
        column_values: List[Set[Value]] = [set() for _ in range(9)]

        for subsquare_y in range(3):
            row_values: List[Set[Value]] = [set() for _ in range(3)]

            for subsquare_x in range(3):
                if not self._is_subsquare_valid(row_values, column_values, subsquare_x * 3, subsquare_y * 3):
                    return False

        return True

    def load(self, something: Any) -> None:
        # TODO: implement
        pass
