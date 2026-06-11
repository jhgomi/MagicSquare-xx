"""Control — Logic·UI Track 조율. 도메인 규칙·입출력 변환은 각 Track에 위임."""

from boundary.grid_io import build_validation_result, flatten_grid
from entity.line_logic import (
    failed_lines,
    has_blank_cells,
    has_duplicate_values,
    has_invalid_values,
)


def validate_lines(grid: list) -> dict:
    """4×4 격자 10선 검증.

    Returns:
        {"status": "pass" | "fail" | "incomplete", "failed_lines": list[str]}
        - pass / incomplete: failed_lines == []
        - fail: 깨진 축 ID (R1~R4, C1~C4, D1, D2)
    """
    flat = flatten_grid(grid)

    if has_blank_cells(flat):
        return build_validation_result("incomplete", [])

    if has_invalid_values(flat) or has_duplicate_values(flat):
        failed = failed_lines(grid)
        return build_validation_result("fail", failed)

    failed = failed_lines(grid)
    if failed:
        return build_validation_result("fail", failed)

    return build_validation_result("pass", [])
