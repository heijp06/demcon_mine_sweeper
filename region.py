from __future__ import annotations
from collections import Counter, defaultdict
from typing import Iterable
import constraint as c


class Region:
    def __init__(self, cells: Iterable[tuple[int, int]], constraints: tuple[int, list[tuple[int, int]]]) -> None:
        self.cells: set[tuple[int, int]] = set(cells)
        self.constraints = list(constraints)

    def __contains__(self, cell: tuple[int, int]) -> bool:
        return cell in self.cells

    def __or__(self, other: Region) -> Region:
        return Region(self.cells | other.cells, self.constraints + other.constraints)

    def get_cell_values(self) -> dict[tuple[int, int], dict[int, int]]:
        problem = c.Problem()
        for value, cells in self.constraints:
            problem.addConstraint(c.ExactSumConstraint(value), cells)
        problem.addVariables(self.cells, [0, 1])
        solutions = problem.getSolutions()
        counts = defaultdict(Counter)
        for cell, value in [pair for solution in solutions for pair in solution.items()]:
            counts[cell].update([value])
        return counts
