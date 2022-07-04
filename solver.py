from itertools import combinations
from typing import Optional
import mineField as mf

UNKNOWN = -1
MINE = -2


class Solver:
    def __init__(self, width: int, height: int, number_of_mines: int) -> None:
        self.width = width
        self.height = height
        self.number_of_mines = number_of_mines
        self.mine_field = mf.MineField(
            **{'width': width, 'height': height, 'number_of_mines': number_of_mines})
        self.grid = [[UNKNOWN] * self.width for _ in range(self.height)]
        self._sweepers = [
            self.sweep_middle_cell,
            self.sweep_cells_for_which_all_mines_are_found,
            self.mark_mines_if_sum_of_adjacent_mines_and_unknowns_equals_cell_value,
            self.try_all_configurations_of_mines_around_cell
        ]

    def sweep(self) -> str:
        for sweeper in self._sweepers:
            result = sweeper()
            if result:
                return result

    def sweep_cells_for_which_all_mines_are_found(self) -> Optional[str]:
        for (row, column) in ((r, c) for r in range(self.height) for c in range(self.width)):
            if self.grid[row][column] in (UNKNOWN, MINE):
                continue
            unknowns = self.get_adjacent_cells(row, column, UNKNOWN)
            if not unknowns:
                continue
            mines = self.get_adjacent_cells(row, column, MINE)
            if len(mines) == self.grid[row][column]:
                for (c, r) in unknowns:
                    self.grid[r][c] = self.mine_field.sweep_cell(c, r)
                return f"Clear all cells around ({column}, {row}) because all the mines there are found."
        return None

    def sweep_middle_cell(self) -> Optional[str]:
        column, row = (self.width - 1) // 2, (self.height - 1) // 2
        if self.grid[row][column] != UNKNOWN:
            return None
        mines = self.mine_field.sweep_cell(column, row)
        self.grid[row][column] = mines
        plural = 's' if mines != 1 else ''
        return f"Sweep middle cell: ({column}, {row}) is surrounded by {mines} mine{plural}."

    def mark_mines_if_sum_of_adjacent_mines_and_unknowns_equals_cell_value(self) -> Optional[str]:
        for (row, column) in ((r, c) for r in range(self.height) for c in range(self.width)):
            cell_value = self.grid[row][column]
            if cell_value in (UNKNOWN, MINE):
                continue
            unknowns = self.get_adjacent_cells(row, column, UNKNOWN)
            if not unknowns:
                continue
            mines = self.get_adjacent_cells(row, column, MINE)
            if len(unknowns) + len(mines) == cell_value:
                for c, r in unknowns:
                    self.grid[r][c] = MINE
                return f"Mark all unknown cells around ({column}, {row}) as mine to get to a total of {cell_value}."
        return None

    def try_all_configurations_of_mines_around_cell(self) -> Optional[str]:
        for (row, column) in ((r, c) for r in range(self.height) for c in range(self.width)):
            cell_value = self.grid[row][column]
            if cell_value in (UNKNOWN, MINE):
                continue
            unknowns = set(self.get_adjacent_cells(row, column, UNKNOWN))
            if not unknowns:
                continue
            cells_to_check = [
                (c, r)
                for (c, r)
                in self.get_adjacent_cells(row, column)
                if self.grid[r][c] not in [MINE, UNKNOWN]
            ]
            number_of_mines = len(self.get_adjacent_cells(row, column, MINE))
            mines_to_add = cell_value - number_of_mines
            cleared = set(unknowns)
            mines = set(unknowns)
            for choice in combinations(unknowns, mines_to_add):
                for c, r in unknowns:
                    self.grid[r][c] = 0
                for c, r in choice:
                    self.grid[r][c] = MINE
                valid = True
                for c, r in cells_to_check:
                    if not self.cell_is_valid(r, c):
                        valid = False
                        break
                for c, r in unknowns:
                    self.grid[r][c] = UNKNOWN
                if valid:
                    mines = mines.intersection(choice)
                    cleared = cleared.intersection(unknowns.difference(choice))
                    if not mines and not cleared:
                        break
            if mines or cleared:
                for c, r in mines:
                    self.grid[r][c] = MINE
                for c, r in cleared:
                    self.grid[r][c] = self.mine_field.sweep_cell(c, r)
                return f"Around ({column, row}) mark mines at {mines} and clear {cleared}."
        return None

    def get_adjacent_cells(self, row, column, cell_type=None) -> list[tuple[int, int]]:
        return [
            (column + dc, row + dr)
            for dr in [-1, 0, 1]
            for dc in [-1, 0, 1]
            if (dc, dr) != (0, 0)
            and 0 <= row + dr < self.height
            and 0 <= column + dc < self.width
            and (cell_type is None or self.grid[row + dr][column + dc] == cell_type)
        ]

    def mines_found(self) -> list[tuple[int, int]]:
        return [
            (column, row)
            for row in range(self.height)
            for column in range(self.width)
            if self.grid[row][column] == MINE
        ]

    def cell_is_valid(self, row, column) -> bool:
        cell_value = self.grid[row][column]
        if cell_value in (MINE, UNKNOWN):
            return True
        number_of_mines = len(self.get_adjacent_cells(row, column, MINE))
        number_of_unknowns = len(self.get_adjacent_cells(row, column, UNKNOWN))
        return number_of_mines <= cell_value <= number_of_mines + number_of_unknowns
