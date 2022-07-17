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


# # solver = Solver(**mf.BEGINNER_FIELD)
# # solver = Solver(**mf.INTERMEDIATE_FIELD)
# solver = Solver(**mf.EXPERT_FIELD)
# print(f"MineSweeper: {solver.width} columns, {solver.height} rows, {solver.number_of_mines} mines")
# print_grid(solver.grid)

# result = solver.sweep()
# while result:
#     print(result)
#     print_grid(solver.grid)
#     try:
#         result = solver.sweep()
#     except mf.ExplosionException:
#         print(f"Mines found at {solver.mines_found()}")
#         print("Mine exploded!!!")
#         break
#     mines = solver.mines_found()
#     if len(mines) == solver.number_of_mines:
#         print(f"Mines found at {solver.mines_found()}")
#         print(f"All mines found.")
#         break

wins = 0
games = 0
for c in range(100):
    print(f"{c} ")
    games += 1
    solver = Solver(**mf.EXPERT_FIELD)
    result = solver.sweep()
    while result:
        try:
            result = solver.sweep()
        except mf.ExplosionException:
            break
        mines = solver.mines_found()
        if len(mines) == solver.number_of_mines:
            wins += 1
            break
print(f"{games} games played, {wins} won ({wins * 100 / games}%).")