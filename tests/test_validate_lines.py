from entity.constants import GRID_SIZE, MAGIC_CONSTANT
from validate_lines import validate_lines


def test_t_inc_01_grid_with_zero(grid_g1):
    # Given — grid_g1, 0 포함 4×4
    grid = [
        grid_g1[i : i + GRID_SIZE]
        for i in range(0, GRID_SIZE * GRID_SIZE, GRID_SIZE)
    ]

    # When
    result = validate_lines(grid)

    # Then
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []


def test_t_inc_01_grid_with_zero_golden(grid_g1):
    # Given — grid_g1, 0 포함 4×4
    grid = [
        grid_g1[i : i + GRID_SIZE]
        for i in range(0, GRID_SIZE * GRID_SIZE, GRID_SIZE)
    ]

    # When
    result = validate_lines(grid)

    # Then — approval
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _approval import assert_matches_golden
    from boundary.golden_format import format_golden

    int6 = [1, 3, 4, 4, 0, 0]  # 1-index blank coords + padding
    assert_matches_golden("T-INC-01", format_golden(result, int6))


def test_t_fail_d1_diagonal_only_wrong(grid_semi_magic_fake):
    # Given — 행·열 34, D1(주대각) 깨짐 4×4
    grid = grid_semi_magic_fake

    # When
    result = validate_lines(grid)

    # Then
    assert result["status"] == "fail"
    assert "D1" in result["failed_lines"]


def test_t_fail_d1_diagonal_only_wrong_golden(grid_semi_magic_fake):
    # Given — 행·열 34, D1(주대각) 깨짐 4×4
    grid = grid_semi_magic_fake

    # When
    result = validate_lines(grid)

    # Then — approval
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _approval import assert_matches_golden
    from boundary.golden_format import format_golden

    int6 = [0, 0, 0, 0, 0, 0]  # 빈칸 없음 — padding
    assert_matches_golden("T-FAIL-D1", format_golden(result, int6))


def test_t_fail_fake_rows_cols_only(grid_semi_magic_fake):
    # Given — 행·열만 34 (가짜 완료), 대각선 미충족
    grid = grid_semi_magic_fake

    # When
    result = validate_lines(grid)

    # Then
    assert result["status"] == "fail"
    assert result["failed_lines"] != []


def test_t_fail_fake_rows_cols_only_golden(grid_semi_magic_fake):
    # Given — 행·열만 34 (가짜 완료), 대각선 미충족
    grid = grid_semi_magic_fake

    # When
    result = validate_lines(grid)

    # Then — approval
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _approval import assert_matches_golden
    from boundary.golden_format import format_golden

    int6 = [0, 0, 0, 0, 0, 0]  # 빈칸 없음 — padding
    assert_matches_golden("T-FAIL-FAKE", format_golden(result, int6))


def test_t_pass_01_complete_magic_square(grid_magic_pass):
    # Given — 0 없음, 1~16 중복 없음, 10선 모두 34
    grid = grid_magic_pass

    # When
    result = validate_lines(grid)

    # Then
    assert result["status"] == "pass"
    assert result["failed_lines"] == []


def test_t_pass_01_complete_magic_square_golden(grid_magic_pass):
    # Given — 0 없음, 1~16 중복 없음, 10선 모두 34
    grid = grid_magic_pass

    # When
    result = validate_lines(grid)

    # Then — approval
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _approval import assert_matches_golden
    from boundary.golden_format import format_golden

    int6 = [0, 0, 0, 0, 0, 0]  # 빈칸 없음 — padding
    assert_matches_golden("T-PASS-01", format_golden(result, int6))
