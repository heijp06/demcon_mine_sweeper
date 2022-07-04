from numpy import mat
import mineField as mf
from solver import MINE, UNKNOWN, Solver


def print_grid(grid: list[list[int]]) -> None:
    for row in grid:
        for column in row:
            if column == MINE:
                print('*', end='')
            elif column == UNKNOWN:
                print('.', end='')
            elif column == 0:
                print(' ', end='')
            else:
                print(str(column), end='')
        print()


# solver = Solver(**mf.BEGINNER_FIELD)
# solver = Solver(**mf.INTERMEDIATE_FIELD)
solver = Solver(**mf.EXPERT_FIELD)
print(f"MineSweeper: {solver.width} columns, {solver.height} rows, {solver.number_of_mines} mines")
print_grid(solver.grid)

result = solver.sweep()
while result:
    print(result)
    print_grid(solver.grid)
    result = solver.sweep()
    mines = solver.mines_found()
    if len(mines) == solver.number_of_mines:
        print(f"Solved, mines are at {mines}.")
        break
