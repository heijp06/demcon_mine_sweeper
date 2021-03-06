import pytest
from unittest.mock import call, MagicMock
from mineField import MineField
from solver import MINE, UNKNOWN, Solver


def test_sweep_corner_cell():
    solver = Solver(3, 4, 1)
    solver.mine_field = MagicMock(spec=MineField)
    for _ in range(4):
        solver.sweep_corner_cell()
    assert_cells_swept(solver, [(0, 0), (0, 3), (2, 0), (2, 3)])


@pytest.mark.parametrize("grid,number_of_mines,mines,cleared,use_total_rule", [
    ([
        [1, 1, UNKNOWN],
        [1, UNKNOWN, UNKNOWN]], 1, [(1, 1)], [(2, 0), (2, 1)], False),
    ([
        [0, UNKNOWN, UNKNOWN],
        [UNKNOWN, UNKNOWN, UNKNOWN]], 1, [], [(1, 0), (0, 1), (1, 1)], False),
    ([
        [1, MINE, UNKNOWN],
        [UNKNOWN, UNKNOWN, UNKNOWN]], 2, [], [(0, 1), (1, 1)], False),
    ([
        [1, UNKNOWN, UNKNOWN],
        [1, UNKNOWN, UNKNOWN],
        [1, UNKNOWN, UNKNOWN]], 3, [(1, 1)], [(1, 0), (1, 2)], False),
    ([
        [1, UNKNOWN, UNKNOWN],
        [2, UNKNOWN, UNKNOWN],
        [1, UNKNOWN, UNKNOWN]], 3, [(1, 0), (1, 2)], [(1, 1)], False),
    ([
        [0, 0, UNKNOWN, UNKNOWN],
        [0, 0, UNKNOWN, UNKNOWN],
        [UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN],
        [UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN]], 1, [], [], False),
    ([
        [UNKNOWN, UNKNOWN, 1],
        [UNKNOWN, UNKNOWN, 2],
        [1, 2, MINE]], 2, [(1, 1)], [(0, 0), (1, 0), (0, 1)], True)
])
def test_sweep_constraint(grid, number_of_mines, mines, cleared, use_total_rule):
    solver = create_solver(grid, number_of_mines, use_total_rule)
    solver.sweep_constraint()
    for column, row in mines:
        assert grid[row][column] == MINE
    for column, row in cleared:
        assert grid[row][column] not in (MINE, UNKNOWN)


@pytest.mark.parametrize("grid,number_of_mines,candidates", [
    ([
        [1, UNKNOWN],
        [UNKNOWN, UNKNOWN]], 1, [(1, 0), (0, 1), (1, 1)]),
])
def test_sweep_random_cell(grid, number_of_mines, candidates):
    solver = create_solver(grid, number_of_mines)
    solver.sweep_random_cell()
    solver.mine_field.sweep_cell.assert_called_once()
    assert solver.mine_field.sweep_cell.call_args.args in candidates


def assert_cells_swept(solver: Solver, cells: list[tuple[int, int]]) -> None:
    assert solver.mine_field.sweep_cell.call_count == len(cells)
    solver.mine_field.sweep_cell.assert_has_calls(
        [call(*cell) for cell in cells], any_order=True)


def create_solver(grid: list[list[int]], number_of_mines: int, use_total_rule: bool = False) -> None:
    width = len(grid[0])
    height = len(grid)
    solver = Solver(width, height, number_of_mines, use_total_rule)
    solver.mine_field = MagicMock(spec=MineField)
    solver.grid = grid
    for column in range(solver.width):
        for row in range(solver.height):
            if solver.grid[row][column] == UNKNOWN:
                continue
            solver.add_active_cells_at(column, row)
    return solver
