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


@pytest.mark.parametrize("grid,number_of_mines,cells", [
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
def test_mark_mines_if_sum_of_adjacent_mines_and_unknowns_equals_cell_value(grid, number_of_mines, cells):
    solver = create_solver(grid, number_of_mines)
    solver.mark_mines_if_sum_of_adjacent_mines_and_unknowns_equals_cell_value()
    for column, row in cells:
        assert grid[row][column] == MINE


@pytest.mark.parametrize("grid,number_of_mines,mines,cleared", [
    ([
        [1, UNKNOWN, UNKNOWN],
        [1, UNKNOWN, UNKNOWN],
        [1, UNKNOWN, UNKNOWN]], 3, [(1, 1)], [(1, 0), (1, 2)]),
    ([
        [1, UNKNOWN, UNKNOWN],
        [2, UNKNOWN, UNKNOWN],
        [1, UNKNOWN, UNKNOWN]], 3, [(1, 0), (1, 2)], [(1, 1)]),
])
def test_try_all_configurations_of_mines_around_cell(grid, number_of_mines, mines, cleared):
    solver = create_solver(grid, number_of_mines)
    solver.try_all_configurations_of_mines_around_cell()
    for column, row in mines:
        assert grid[row][column] == MINE
    for column, row in cleared:
        assert grid[row][column] not in (MINE, UNKNOWN)


def assert_cells_swept(solver: Solver, cells: list[tuple[int, int]]) -> None:
    assert solver.mine_field.sweep_cell.call_count == len(cells)
    solver.mine_field.sweep_cell.assert_has_calls(
        [call(*cell) for cell in cells], any_order=True)


def create_solver(grid: list[list[int]], number_of_mines: int) -> None:
    width = len(grid[0])
    height = len(grid)
    solver = Solver(width, height, number_of_mines)
    solver.mine_field = MagicMock(spec=MineField)
    solver.grid = grid
    return solver
