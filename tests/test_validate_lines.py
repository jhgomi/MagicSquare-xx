import pytest

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

    # Then — assert 금지; RED 스켈레톤만
    pytest.fail(
        f"RED: T-INC-01 — expect status incomplete, failed_lines [] (MAGIC={MAGIC_CONSTANT})"
    )


def test_t_fail_d1_diagonal_only_wrong(grid_semi_magic_fake):
    # Given — 행·열 34, D1(주대각) 깨짐 4×4
    grid = grid_semi_magic_fake

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail("RED: T-FAIL-D1 — expect status fail, D1 in failed_lines")


def test_t_fail_fake_rows_cols_only(grid_semi_magic_fake):
    # Given — 행·열만 34 (가짜 완료), 대각선 미충족
    grid = grid_semi_magic_fake

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail(
        "RED: T-FAIL-FAKE — expect status fail (pass forbidden), rows/cols only 34"
    )


def test_t_pass_01_complete_magic_square(grid_magic_pass):
    # Given — 0 없음, 1~16 중복 없음, 10선 모두 34
    grid = grid_magic_pass

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail(
        f"RED: T-PASS-01 — expect status pass, failed_lines [] (MAGIC={MAGIC_CONSTANT})"
    )
