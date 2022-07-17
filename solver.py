import random
from typing import Optional

import mineField as mf

from region import Region

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
        regions = []
        for column, row in self.active_cells:
            value = self.grid[row][column]
            if value in (UNKNOWN, MINE):
                continue
            cells = self.get_adjacent_cells(column, row, is_unknown)
            number_of_mines = len(
                self.get_adjacent_cells(column, row, is_mine))
            new_region = Region(cells, [(value - number_of_mines, cells)])
            new_regions = []
            for region in regions:
                if any(cell in region for cell in cells):
                    new_region |= region
                else:
                    new_regions.append(region)
            new_regions.append(new_region)
            regions = new_regions
        cells_with_mines = []
        cells_without_mines = []
        for region in regions:
            counts = region.get_cell_values()
            for (column, row), chance in counts.items():
                if chance == 0.0:
                    self.add_active_cells_at(column, row)
                    cells_without_mines.append((column, row))
                    self.grid[row][column] = self.mine_field.sweep_cell(
                        column, row)
                if chance == 1.0:
                    self.add_active_cells_at(column, row)
                    self.add_active_cells_at(column, row)
                    cells_with_mines.append((column, row))
                    self.grid[row][column] = MINE
        if cells_with_mines or cells_without_mines:
            return f"Mines at: {cells_with_mines}, no mines at: {cells_without_mines}"
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
