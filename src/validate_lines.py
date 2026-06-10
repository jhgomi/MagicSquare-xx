from entity.constants import CELL_MAX, GRID_SIZE, MAGIC_CONSTANT

LINE_IDS = [
    "R1", "R2", "R3", "R4",
    "C1", "C2", "C3", "C4",
    "D1", "D2",
]


def _failed_lines(grid: list) -> list[str]:
    failed: list[str] = []
    n = GRID_SIZE
    for i in range(n):
        if sum(grid[i]) != MAGIC_CONSTANT:
            failed.append(f"R{i + 1}")
    for j in range(n):
        if sum(grid[i][j] for i in range(n)) != MAGIC_CONSTANT:
            failed.append(f"C{j + 1}")
    if sum(grid[i][i] for i in range(n)) != MAGIC_CONSTANT:
        failed.append("D1")
    if sum(grid[i][n - 1 - i] for i in range(n)) != MAGIC_CONSTANT:
        failed.append("D2")
    return failed


def validate_lines(grid: list) -> dict:
    """4×4 격자 10선 검증.

    Returns:
        {"status": "pass" | "fail" | "incomplete", "failed_lines": list[str]}
        - pass / incomplete: failed_lines == []
        - fail: 깨진 축 ID (R1~R4, C1~C4, D1, D2)
    """
    flat = [cell for row in grid for cell in row]

    if 0 in flat:
        return {"status": "incomplete", "failed_lines": []}

    if any(v < 1 or v > CELL_MAX for v in flat):
        failed = _failed_lines(grid)
        return {"status": "fail", "failed_lines": failed}

    if len(set(flat)) != len(flat):
        failed = _failed_lines(grid)
        return {"status": "fail", "failed_lines": failed}

    failed = _failed_lines(grid)
    if failed:
        return {"status": "fail", "failed_lines": failed}

    return {"status": "pass", "failed_lines": []}
