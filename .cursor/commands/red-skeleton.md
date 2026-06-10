# red-skeleton

ARRR **A단계 (RED ④)** — `/red-test-plan` 설계표(블록 1~3) 기준으로 **pytest.fail 스켈레톤만** 작성한다.

**magic-square-tdd Skill이 있으면 자동 따름** (픽스처·명명·AAA·상수 import 규칙 우선).

SSOT: 직전 `/red-test-plan` 출력 · `.cursorrules` · `docs/PRD.md`(있으면)

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: red | Layer: entity | Track: Logic
```

| 항목 | 값 | 기본 |
|------|-----|------|
| **Phase** | `red` | 고정 (GREEN·REFACTOR 금지) |
| **Layer** | `entity` \| `boundary` | `/red-test-plan`과 동일 |
| **Track** | `Logic` \| `UI` | `/red-test-plan`과 동일 |

**Track A (boundary):** `Layer: boundary`만 바꾸면 본 Command를 **그대로 재사용**한다.

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `tests/` — 테스트 함수·`conftest.py` 스켈레톤 | `src/` 전체 (`validate_lines.py` 등) |
| `entity/constants.py` — **상수 정의만** (34·16·4) | `assert` 본문·기대값 검증 |
| AAA 주석 (`# Given` / `# When` / `# Then`) | `@pytest.mark.skip`, `pytest.skip`, `xfail` |
| `pytest.fail("RED: {Test ID} — …")` 한 줄 (Then) | 통과 더미 (`pass`, `return`, `assert True`) |
| | GREEN / REFACTOR |
| | Domain Mock (Logic Track) |
| | git commit (사용자 요청 시만) |

---

## 선행 조건

- 채팅에 `/red-test-plan` **블록 1~3**이 없으면, SSOT(`.cursorrules`·`Report/03`)로 **동일 형식 플랜을 먼저 요약**한 뒤 스켈레톤을 쓴다. 사용자에게 Test ID 재질문 금지.
- **RED 묶음 범위**(블록 3)에 있는 Test ID만 이번에 스켈레톤화한다. 한 사이클에 **Test ID 하나**만 해도 된다.

---

## AAA 스켈레톤 규칙

각 테스트 = **한 Test ID** = **한 행동·한 검증**.

1. **Given** — 격자·픽스처·상수. `0`=빈칸. 마법상수·크기는 **리터럴 금지** → `entity.constants` import.
2. **When** — 설계표의 Act (예: `result = validate_lines(grid)`). 구현이 없어도 호출 줄은 둔다.
3. **Then** — **아래 한 줄만** (assert·pass 금지):

```python
pytest.fail("RED: {Test ID} — {설계표 Then 요약}")
```

---

## 상수·픽스처

### entity/constants.py

테스트·픽스처 데이터에서만 사용. `src/`가 아닌 `entity/` 패키지.

```python
MAGIC_CONSTANT = 34
GRID_SIZE = 4
CELL_MAX = 16
```

이미 있으면 수정하지 않고 import만 한다.

### tests/conftest.py — `grid_g1`

| 항목 | 내용 |
|------|------|
| **이름** | `grid_g1` |
| **형식** | row-major flat `list[int]` 길이 16 (또는 4×4 중첩 — 설계표 명시 따름) |
| **빈칸** | `0` **정확히 2개** |
| **용도** | incomplete·빈칸 좌표·row-major 경계 케이스 Given |

```python
import pytest

from entity.constants import GRID_SIZE


@pytest.fixture
def grid_g1() -> list[int]:
    """row-major 4×4, 0 두 개 — T-INC / blank-coords RED Given."""
    return [
        16, 3, 0, 13,
        5, 10, 11, 8,
        9, 6, 7, 12,
        4, 15, 14, 0,
    ]
```

설계표에 다른 픽스처명이 있으면 `/red-test-plan` 블록 3을 우선한다.

---

## Test ID ↔ 함수명 매핑

| Test ID (예) | 함수명 (예) |
|--------------|-------------|
| T-INC-01 | `test_t_inc_01_grid_with_zero` |
| T-FAIL-D1 | `test_t_fail_d1_diagonal_only_wrong` |
| `D-LOC-01` | `test_d_loc_01_blank_coords_row_major` |

규칙: `test_<snake_case>` — Test ID를 소문자·`_`로 변환. **1 Test ID : 1 함수**.

---

## 템플릿 예시 — `test_d_loc_01_blank_coords_row_major`

```python
import pytest

from entity.constants import GRID_SIZE, MAGIC_CONSTANT
from validate_lines import validate_lines


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given — row-major grid_g1, 0 두 칸; GRID_SIZE=4
    n = GRID_SIZE
    grid = [
        grid_g1[0:n],
        grid_g1[n : 2 * n],
        grid_g1[2 * n : 3 * n],
        grid_g1[3 * n : 4 * n],
    ]
    blank_indices = [i for i, v in enumerate(grid_g1) if v == 0]

    # When — validate_lines 호출 (RED: 구현 전)
    result = validate_lines(grid)

    # Then — assert 금지; RED 스켈레톤만
    pytest.fail(
        f"RED: D-LOC-01 — blank coords row-major {blank_indices}; "
        f"expect status incomplete, failed_lines [] (MAGIC={MAGIC_CONSTANT})"
    )
```

- **Then**에 `pytest.fail` **한 줄**만 (f-string 허용).
- 메시지에 Test ID·설계 Then 요약을 반드시 포함.

### validate_lines 계열 (세션 3 기본) 스켈레톤

```python
def test_t_inc_01_grid_with_zero(grid_g1):
    # Given — grid_g1, 0 포함 4×4
    grid = [grid_g1[i : i + GRID_SIZE] for i in range(0, GRID_SIZE * GRID_SIZE, GRID_SIZE)]

    # When
    result = validate_lines(grid)

    # Then
    pytest.fail("RED: T-INC-01 — expect status incomplete, failed_lines []")
```

---

## 작업 절차

1. `/red-test-plan` 블록 3 **RED 묶음** Test ID 확인.
2. `tests/conftest.py`에 `grid_g1` 없으면 추가.
3. `entity/constants.py` 없으면 상수만 생성 (34·16·4).
4. 대상 `tests/test_*.py`에 AAA + `pytest.fail` 스켈레톤 추가·교체 (`...`·`pass` 제거).
5. pytest 실행 후 보고.

---

## pytest 실행

```bash
python -m pytest tests/ -v
```

또는 묶음 범위만:

```bash
python -m pytest tests/test_validate_lines.py::test_t_inc_01_grid_with_zero -v
```

**성공 기준:** 해당 Test ID 테스트가 **FAILED** — `pytest.fail` 메시지로 실패. **PASSED면 스켈레톤 오류** (통과 더미·assert 잔존·구현이 이미 GREEN).

---

## 완료 보고 형식

작업 후 **pytest를 실행**하고 아래 3항을 반드시 보고한다:

1. **Test ID** — 이번 스켈레톤화한 ID
2. **FAIL 한 줄** — `FAIL — RED: {Test ID} — …`
3. **변경 파일** — `tests/`(및 없었을 때만 `entity/constants.py`) 목록

```
Phase: red | Layer: entity | Track: Logic

## 변경 (tests/만)
- tests/conftest.py: grid_g1
- tests/test_validate_lines.py: test_t_inc_01_grid_with_zero (T-INC-01)

## pytest
- 명령: python -m pytest tests/test_validate_lines.py::test_t_inc_01_grid_with_zero -v
- T-INC-01 · FAIL — RED: T-INC-01 — expect status incomplete, failed_lines []

## 다음
- /tdd-red: pytest.fail → assert 본문
```

마지막 한 줄:

```
/tdd-red 으로 넘길 준비됐다
```

---

## 금지 (재확인)

- `src/` 수정·생성
- `assert`·`self.assert*`·통과 더미
- `@pytest.mark.skip`, `pytest.skip`, `xfail`
- Then에 `pytest.fail` 외 코드
- GREEN / REFACTOR
- Logic Track Domain Mock
- `34`·`16`·`4` 리터럴 (픽스처·테스트 본문) — `entity.constants` import 필수

## 다음 단계

- RED **실패 테스트**(assert) 완성: `/tdd-red`
- 구현: GREEN (별도 명령·세션)
