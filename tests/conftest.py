import pytest

from entity.constants import GRID_SIZE


@pytest.fixture
def grid_g1() -> list[int]:
    """row-major 4×4, 0 두 개 — T-INC-01 RED Given."""
    return [
        16, 3, 0, 13,
        5, 10, 11, 8,
        9, 6, 7, 12,
        4, 15, 14, 0,
    ]


@pytest.fixture
def grid_semi_magic_fake() -> list[list[int]]:
    """행·열 합 34, 대각선 깨짐 — T-FAIL-D1 · T-FAIL-FAKE Given."""
    return [
        [5, 10, 11, 8],
        [16, 3, 2, 13],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]


@pytest.fixture
def grid_magic_pass() -> list[list[int]]:
    """정답 4×4 마방진 — T-PASS-01 Given."""
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
