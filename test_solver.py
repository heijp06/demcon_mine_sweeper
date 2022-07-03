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
    width = len(grid[0])
    height = len(grid)
    solver = Solver(width, height, 2)
    solver.mine_field = MagicMock(spec=MineField)
    solver.grid = grid
    solver.sweep_cells_for_which_all_mines_are_found()
    assert_cells_swept(solver, cells)


def assert_cells_swept(solver: Solver, cells: list[tuple[int, int]]) -> None:
    assert solver.mine_field.sweep_cell.call_count == len(cells)
    solver.mine_field.sweep_cell.assert_has_calls(
        [call(*cell) for cell in cells], any_order=True)
