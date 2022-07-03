from decimal import MIN_EMIN
import pytest
from unittest.mock import call, MagicMock
from mineField import MineField
from solver import MINE, UNKNOWN, Solver


def test_sweep_middle_cell():
    solver = Solver(3, 3, 1)
    solver.mine_field = MagicMock(spec=MineField)
    solver.sweep_middle_cell()
    assert_cells_swept(solver, [(1, 1)])


@pytest.mark.parametrize("grid,cells", [
    ([
        [0, UNKNOWN, UNKNOWN],
        [UNKNOWN, UNKNOWN, UNKNOWN]], [(1, 0), (0, 1), (1, 1)]),
    ([
        [1, MINE, UNKNOWN],
        [UNKNOWN, UNKNOWN, UNKNOWN]], [(0, 1), (1, 1)])
])
def test_sweep_cells_for_which_all_mines_are_found(grid, cells):
    solver = create_solver(grid, 2)
    solver.sweep_cells_for_which_all_mines_are_found()
    assert_cells_swept(solver, cells)


@pytest.mark.parametrize("grid,mines,cells", [
    ([
        [1, 1, UNKNOWN],
        [1, UNKNOWN, UNKNOWN]], 1, [(1, 1)]),
    ([
        [1, 2, 3, 2, 1],
        [UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN]], 3, [(1, 1), (2, 1), (3, 1)]),
    ([
        [1, 2, 3, 2, 1],
        [UNKNOWN, MINE, UNKNOWN, UNKNOWN, UNKNOWN]], 3, [(2, 1), (3, 1)]),
    ([
        [1, 2, 3, 2, 1],
        [UNKNOWN, UNKNOWN, MINE, MINE, UNKNOWN]], 3, [(1, 1)])
])
def test_mark_mines_if_sum_of_adjacent_mines_and_unknowns_equals_cell_value(grid, mines, cells):
    solver = create_solver(grid, mines)
    solver.mark_mines_if_sum_of_adjacent_mines_and_unknowns_equals_cell_value()
    for column, row in cells:
        assert grid[row][column] == MINE


def assert_cells_swept(solver: Solver, cells: list[tuple[int, int]]) -> None:
    assert solver.mine_field.sweep_cell.call_count == len(cells)
    solver.mine_field.sweep_cell.assert_has_calls(
        [call(*cell) for cell in cells], any_order=True)


def create_solver(grid: list[list[int]], mines: int) -> None:
    width = len(grid[0])
    height = len(grid)
    solver = Solver(width, height, mines)
    solver.mine_field = MagicMock(spec=MineField)
    solver.grid = grid
    return solver
