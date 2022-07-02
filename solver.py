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

    def sweep(self) -> str:
        column, row = self.width // 2, self.height // 2
        if self.grid[row][column] == UNKNOWN:
            mines = self.mine_field.sweep_cell(column, row)
            self.grid[row][column] = mines
            return f"First try: ({column}, {row}) is surrounded by {mines} mine{mines != 1 and 's' or ''}."
        pass
