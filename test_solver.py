from unittest.mock import call, MagicMock
from mineField import MineField
from solver import UNKNOWN, Solver


def test_sweep_middle_cell():
    solver = Solver(3, 3, 1)
    solver.mine_field = MagicMock(spec=MineField)
    solver.sweep_middle_cell()

    solver.mine_field.sweep_cell.assert_called_once_with(1, 1)


def test_sweep_cells_for_which_all_mines_are_found():
    solver = Solver(3, 3, 1)
    solver.mine_field = MagicMock(spec=MineField)
    solver.grid = [
        [0, UNKNOWN, UNKNOWN],
        [UNKNOWN, UNKNOWN, UNKNOWN],
        [UNKNOWN, UNKNOWN, UNKNOWN],
    ]
    solver.sweep_cells_for_which_all_mines_are_found()

    assert solver.mine_field.sweep_cell.call_count == 3
    solver.mine_field.sweep_cell.assert_has_calls(
        [call(1, 0), call(0, 1), call(1, 1)], any_order=True)
