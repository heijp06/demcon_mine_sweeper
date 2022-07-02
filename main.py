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
            else:
                print(str(column), end='')
        print()


# solver = Solver(**mf.BEGINNER_FIELD)
solver = Solver(**mf.INTERMEDIATE_FIELD)
# solver = Solver(**mf.EXPERT_FIELD)
print_grid(solver.grid)

print(solver.sweep())
print_grid(solver.grid)
