"""Logic Track — 10선·셀 값 도메인 규칙."""

from entity.constants import CELL_MAX, GRID_SIZE, MAGIC_CONSTANT

LINE_IDS = [
    "R1", "R2", "R3", "R4",
    "C1", "C2", "C3", "C4",
    "D1", "D2",
]


def has_blank_cells(cells: list[int]) -> bool:
    return 0 in cells


def has_invalid_values(cells: list[int]) -> bool:
    return any(v < 1 or v > CELL_MAX for v in cells)


def has_duplicate_values(cells: list[int]) -> bool:
    return len(set(cells)) != len(cells)


def failed_lines(grid: list) -> list[str]:
    failed: list[str] = []
    n = GRID_SIZE
    for row_idx in range(n):
        if sum(grid[row_idx]) != MAGIC_CONSTANT:
            failed.append(f"R{row_idx + 1}")
    for col_idx in range(n):
        if sum(grid[row_idx][col_idx] for row_idx in range(n)) != MAGIC_CONSTANT:
            failed.append(f"C{col_idx + 1}")
    if sum(grid[d][d] for d in range(n)) != MAGIC_CONSTANT:
        failed.append("D1")
    if sum(grid[d][n - 1 - d] for d in range(n)) != MAGIC_CONSTANT:
        failed.append("D2")
    return failed
