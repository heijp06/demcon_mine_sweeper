from collections import defaultdict
from itertools import combinations
import random
from typing import Counter, Optional
import mineField as mf
import constraint as c

UNKNOWN = -1
MINE = -2


def is_mine(value: int) -> bool:
    return value == MINE


def is_unknown(value: int) -> bool:
    return value == UNKNOWN


class Solver:
    def __init__(self, width: int, height: int, number_of_mines: int) -> None:
        self.width = width
        self.height = height
        self.number_of_mines = number_of_mines
        self.mine_field = mf.MineField(
            **{'width': width, 'height': height, 'number_of_mines': number_of_mines})
        self.grid = [[UNKNOWN] * self.width for _ in range(self.height)]
        self._sweepers = [
            # self.try_all_configurations_of_mines_around_cell,
            self.sweep_constraint,
            self.sweep_corner_cell,
            self.sweep_random_cell
        ]
        self.active_cells: set[tuple[int, int]] = set()

    def sweep(self) -> str:
        for sweeper in self._sweepers:
            result = sweeper()
            if result:
                self.prune_active_cells()
                print(self.active_cells)
                return result

    def sweep_corner_cell(self) -> Optional[str]:
        column, row = next((
            (c, r)
            for (c, r)
            in ((0, 0), (0, self.height - 1), (self.width - 1, 0))
            if self.grid[r][c] == UNKNOWN), (self.width - 1, self.height - 1))
        if self.grid[row][column] != UNKNOWN:
            return None
        self.add_active_cells_at(column, row)
        mines = self.mine_field.sweep_cell(column, row)
        self.grid[row][column] = mines
        plural = 's' if mines != 1 else ''
        return f"Sweep corner cell: ({column}, {row}) is surrounded by {mines} mine{plural}."

    def sweep_constraint(self) -> Optional[str]:
        if not self.active_cells:
            return None
        problem = c.Problem()
        all_variables = set()
        for column, row in self.active_cells:
            value = self.grid[row][column]
            if value in (UNKNOWN, MINE):
                continue
            variables = self.get_adjacent_cells(column, row, is_unknown)
            number_of_mines = len(
                self.get_adjacent_cells(column, row, is_mine))
            problem.addConstraint(c.ExactSumConstraint(
                value - number_of_mines), variables)
            all_variables = all_variables.union(variables)
        problem.addVariables(all_variables, [0, 1])
        solutions = problem.getSolutions()
        counts = defaultdict(Counter)
        for cell, value in [pair for solution in solutions for pair in solution.items()]:
            counts[cell].update([value])
        cells_with_mines = []
        cells_without_mines = []
        for (column, row), values in counts.items():
            if len(values) == 1:
                self.add_active_cells_at(column, row)
                if 0 in values:
                    cells_without_mines.append((column, row))
                    self.grid[row][column] = self.mine_field.sweep_cell(column, row)
                else:
                    cells_with_mines.append((column, row))
                    self.grid[row][column] = MINE
        if not cells_with_mines and not cells_without_mines:
            return None
        return f"Mines at: {cells_with_mines}, no mines at: {cells_without_mines}"


    def try_all_configurations_of_mines_around_cell(self) -> Optional[str]:
        for (column, row) in self.active_cells:
            cell_value = self.grid[row][column]
            if cell_value in (UNKNOWN, MINE):
                continue
            unknowns = set(self.get_adjacent_cells(column, row, is_unknown))
            if not unknowns:
                continue
            cells_to_check = [
                (c, r)
                for (c, r)
                in self.get_adjacent_cells(column, row)
                if self.grid[r][c] not in [MINE, UNKNOWN]
            ]
            number_of_mines = len(
                self.get_adjacent_cells(column, row, is_mine))
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
                    self.add_active_cells_at(c, r)
                    self.grid[r][c] = MINE
                for c, r in cleared:
                    self.add_active_cells_at(c, r)
                    self.grid[r][c] = self.mine_field.sweep_cell(c, r)
                return f"Around ({column, row}) mark mines at {mines} and clear {cleared}."
        return None

    def sweep_random_cell(self):
        column, row = random.choice([
            (c, r)
            for c in range(self.width)
            for r in range(self.height)
            if self.grid[r][c] == UNKNOWN
        ])
        self.add_active_cells_at(column, row)
        self.grid[row][column] = self.mine_field.sweep_cell(column, row)
        return f"Choose random cell ({column}, {row})."

    def add_active_cells_at(self, column, row):
        self.active_cells.add((column, row))
        self.active_cells = self.active_cells.union(
            self.get_adjacent_cells(column, row))

    def get_adjacent_cells(self, column, row, cell_selector=None) -> list[tuple[int, int]]:
        cell_selector = cell_selector or (lambda _: True)
        return [
            (column + dc, row + dr)
            for dr in [-1, 0, 1]
            for dc in [-1, 0, 1]
            if (dc, dr) != (0, 0)
            and 0 <= row + dr < self.height
            and 0 <= column + dc < self.width
            and cell_selector(self.grid[row + dr][column + dc])
        ]

    def prune_active_cells(self) -> None:
        self.active_cells = set(
            (column, row)
            for (column, row)
            in self.active_cells
            if any(self.get_adjacent_cells(column, row, is_unknown))
        )

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
        number_of_mines = len(self.get_adjacent_cells(column, row, is_mine))
        number_of_unknowns = len(
            self.get_adjacent_cells(column, row, is_unknown))
        return number_of_mines <= cell_value <= number_of_mines + number_of_unknowns
