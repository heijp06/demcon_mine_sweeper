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
            self.sweep_cells_for_which_all_mines_are_found
        ]

    def sweep(self) -> str:
        for sweeper in self._sweepers:
            result = sweeper()
            if result:
                return result

    def sweep_cells_for_which_all_mines_are_found(self) -> str:
        for (row, column) in ((r, c) for r in range(self.height) for c in range(self.width)):
            if self.grid[row][column] in (UNKNOWN, MINE):
                continue
            unknowns = [
                (r, c)
                for (r, c) in self.neighbours(row, column)
                if self.grid[r][c] == UNKNOWN
            ]
            if not unknowns:
                continue
            mines = sum(
                self.grid[r][c] == MINE
                for (r, c) in self.neighbours(row, column)
            )
            if mines == self.grid[row][column]:
                for (r, c) in unknowns:
                    self.grid[r][c] = self.mine_field.sweep_cell(c, r)
                return f"Clear all cells around ({row}, {column}) because all the mines there are found."
        return None

    def sweep_middle_cell(self) -> str:
        column, row = (self.width - 1) // 2, (self.height - 1) // 2
        if self.grid[row][column] != UNKNOWN:
            return None
        mines = self.mine_field.sweep_cell(column, row)
        self.grid[row][column] = mines
        plural = 's' if mines != 1 else ''
        return f"Sweep middle cell: ({column}, {row}) is surrounded by {mines} mine{plural}."

    def neighbours(self, row: int, column: int) -> list[tuple[int, int]]:
        return [
            (row + dr, column + dc)
            for dr in [-1, 0, 1]
            for dc in [-1, 0, 1]
            if (dr, dc) != (0, 0)
            and 0 <= row + dr < self.height
            and 0 <= column + dc < self.width
        ]
