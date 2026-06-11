"""UI Track — 격자 입출력·검증 결과 dict 계약."""

from entity.constants import GRID_SIZE


def flatten_grid(grid: list) -> list[int]:
    return [cell for row in grid for cell in row]


def build_validation_result(status: str, failed_lines: list[str]) -> dict:
    return {"status": status, "failed_lines": failed_lines}


def parse_grid_texts(text_rows: list[list[str]]) -> list[list[int]] | None:
    """UI 입력 문자열 행렬 → 4×4 격자. 빈칸은 0, 파싱 실패 시 None."""
    grid: list[list[int]] = []
    for r in range(GRID_SIZE):
        row: list[int] = []
        for c in range(GRID_SIZE):
            text = text_rows[r][c].strip()
            if text == "":
                row.append(0)
                continue
            try:
                row.append(int(text))
            except ValueError:
                return None
        grid.append(row)
    return grid


def format_grid_for_display(grid: list[list[int]]) -> list[list[str]]:
    """4×4 격자 → UI 표시용 문자열 행렬. 0은 빈칸."""
    return [
        ["" if value == 0 else str(value) for value in row]
        for row in grid
    ]
