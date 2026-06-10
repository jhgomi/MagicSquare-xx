from validate_lines import validate_lines


def test_grid_with_zero_returns_incomplete():
    """0(빈칸) 포함 — status incomplete, failed_lines []."""
    ...


def test_diagonal_only_wrong_returns_fail():
    """행·열은 34, 대각선(D1/D2)만 틀림 — status fail, failed_lines에 대각선 포함."""
    ...


def test_rows_cols_only_fake_complete_returns_fail():
    """행·열만 34, 대각선 미충족 — pass 금지, status fail."""
    ...


def test_complete_magic_square_returns_pass():
    """0 없음, 1~16 중복 없음, 10선 모두 34 — status pass, failed_lines []."""
    ...
