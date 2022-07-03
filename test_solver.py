from unittest.mock import call, MagicMock
from mineField import MineField
from solver import UNKNOWN, Solver


def test_sweep_middle_cell():
    solver = Solver(3, 3, 1)
    solver.mine_field = MagicMock(spec=MineField)
    solver.sweep_middle_cell()
    assert_cells_swept(solver, [(1, 1)])


def test_sweep_cells_for_which_all_mines_are_found():
    solver = Solver(3, 2, 1)
    solver.mine_field = MagicMock(spec=MineField)
    solver.grid = [
        [0, UNKNOWN, UNKNOWN],
        [UNKNOWN, UNKNOWN, UNKNOWN],
    ]
    solver.sweep_cells_for_which_all_mines_are_found()
    assert_cells_swept(solver, [(1, 0), (0, 1), (1, 1)])


def assert_cells_swept(solver: Solver, cells: list[tuple[int, int]]) -> None:
    assert solver.mine_field.sweep_cell.call_count == len(cells)
    solver.mine_field.sweep_cell.assert_has_calls(
        [call(*cell) for cell in cells], any_order=True)
