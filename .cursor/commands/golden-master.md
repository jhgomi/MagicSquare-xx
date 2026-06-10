# golden-master

GREEN **PASS** 후 **Golden Master(Approval Test)** 를 구축·검증한다. 회귀 시 출력이 기준과 일치하는지 확인한다.

SSOT: `.cursorrules` · 직전 GREEN 완료 Test ID · `/red-test-plan` 설계표

**magic-square-tdd Skill이 있으면 자동 따름**

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: green | Layer: entity | Track: Logic
```

| 항목 | 값 | 기본 |
|------|-----|------|
| **Phase** | `green` | Golden은 GREEN PASS **이후**만 |
| **Layer** | `entity` \| `boundary` | 기본 `entity` |
| **Track** | `Logic` \| `UI` | 기본 `Logic` |

**Track A (boundary):** `Layer: boundary`만 바꾸면 재사용.

---

## 전제 조건

| 항목 | 요구 |
|------|------|
| **대상 Test ID** | 해당 테스트 **pytest PASS** (GREEN 완료) |
| **구현** | `src/`에 최소 구현 존재 — 스텁·`pytest.fail` 아님 |
| **선행** | `/tdd-red` assert 통과 확인 후 실행 |

전제 미충족 시 Golden 구축 **중단** — RED·스켈레톤 단계로 되돌리지 않고 GREEN 완료를 먼저 보고.

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `tests/_approval.py` — `assert_matches_golden` (없으면 생성) | golden 파일 **수동 편집**으로 matched 우회 |
| `tests/golden/{id}.approved.txt` — **코드·UPDATE_GOLDEN으로만** 생성·갱신 | `@pytest.mark.skip`, `xfail`, assert 완화 |
| 대상 테스트에 approval 호출 추가 | 기준 없이 테스트를 green으로 맞추기 |
| | RED 단계로 되돌리기 (별도 명령) |
| | git commit (사용자 요청 시만) |

---

## Golden 출력 포맷 (고정)

기준 파일·실측 문자열은 **동일 직렬화**를 쓴다. 수동 편집 금지.

### int[6] — 1-index

6개 정수, **1-based** 좌표·인덱스. 예: 빈칸 위치 `(row, col)` 쌍 또는 row-major 1-index.

```
# 형식: 공백 구분 6정수, 1-index
2 4 4 2 0 0
```

| 위치 | 의미 (예: blank-coords) |
|------|-------------------------|
| `[0],[1]` | 첫 번째 `0` — row, col (1-index) |
| `[2],[3]` | 두 번째 `0` — row, col (1-index) |
| `[4],[5]` | 예약·패딩 (미사용 시 `0 0`) |

도메인에 맞지 않으면 Test ID별로 설계표에 정의하되 **항상 6정수·1-index** 유지.

### 에러 코드 문자열

한 줄 고정. `status` + `failed_lines` 직렬화:

```
ERR status={pass|fail|incomplete} failed={R1,C2,D1|none}
```

| 필드 | 규칙 |
|------|------|
| `status` | `pass` \| `fail` \| `incomplete` |
| `failed` | 깨진 축 ID를 `,` 구분·**알파벳순**; 없으면 `none` |

### 전체 `.approved.txt` 예시 (`t-inc-01`)

```
INT6 1 3 4 2 0 0
ERR status=incomplete failed=none
```

- 줄 순서·접두어(`INT6`, `ERR`) 고정.
- 직렬화 함수는 `tests/_approval.py`에 **한 곳**만 둔다.

---

## 절차 (순서 고정)

### 1. `assert_matches_golden` 준비

`tests/_approval.py` 없으면 생성. 핵심 API:

```python
from pathlib import Path
import os

GOLDEN_DIR = Path(__file__).parent / "golden"


def format_golden(actual: dict, int6: list[int]) -> str:
    """int[6] 1-index + ERR 한 줄 — 포맷 고정."""
    failed = ",".join(sorted(actual["failed_lines"])) if actual["failed_lines"] else "none"
    int6_line = "INT6 " + " ".join(str(x) for x in int6)
    err_line = f"ERR status={actual['status']} failed={failed}"
    return f"{int6_line}\n{err_line}\n"


def assert_matches_golden(test_id: str, actual_text: str) -> None:
    """UPDATE_GOLDEN=1 이면 기준 생성; 아니면 diff 비교."""
    golden_path = GOLDEN_DIR / f"{test_id.lower()}.approved.txt"
    golden_path.parent.mkdir(parents=True, exist_ok=True)

    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.write_text(actual_text, encoding="utf-8")
        return

    if not golden_path.exists():
        raise AssertionError(f"golden missing: {golden_path} — run UPDATE_GOLDEN=1 first")

    expected = golden_path.read_text(encoding="utf-8")
    if actual_text != expected:
        raise AssertionError(
            f"golden mismatch: {golden_path}\n--- expected ---\n{expected}--- actual ---\n{actual_text}"
        )
```

### 2. `tests/golden/{id}.approved.txt` 연결

| 항목 | 규칙 |
|------|------|
| **경로** | `tests/golden/{test_id}.approved.txt` |
| **{id}** | Test ID 소문자 (예: `T-INC-01` → `t-inc-01.approved.txt`) |
| **연결** | 대상 테스트 Then에서 `format_golden` → `assert_matches_golden(test_id, text)` |

```python
def test_t_inc_01_grid_with_zero_golden(grid_g1):
    # Given / When — GREEN PASS와 동일
    result = validate_lines(grid)
    int6 = [1, 3, 4, 2, 0, 0]  # 1-index blank coords + padding

    # Then — approval
    from _approval import assert_matches_golden, format_golden

    assert_matches_golden("T-INC-01", format_golden(result, int6))
```

### 3. 기준 파일 생성 — `UPDATE_GOLDEN=1`

```bash
UPDATE_GOLDEN=1 python -m pytest tests/test_validate_lines.py::test_t_inc_01_grid_with_zero_golden -v
```

- **PASS**여야 함 (기준 쓰기만, assert 실패 없음).
- 생성된 `tests/golden/t-inc-01.approved.txt` 내용을 **수동 수정하지 않는다**.

### 4. matched 확인 — `UPDATE_GOLDEN` 없이

```bash
python -m pytest tests/test_validate_lines.py::test_t_inc_01_grid_with_zero_golden -v
```

- **PASS** = matched.
- **FAIL** = diff 발생 — `src/` 또는 직렬화 로직 점검. golden 수동 편집 **금지**.

---

## 작업 절차 요약

1. 대상 Test ID **pytest PASS** 확인.
2. `tests/_approval.py` 존재·`assert_matches_golden` 연결.
3. golden approval 테스트 함수 추가 (기존 PASS 테스트와 분리 또는 확장).
4. `UPDATE_GOLDEN=1 pytest …` 로 `.approved.txt` 생성.
5. `UPDATE_GOLDEN` 없이 재실행 → matched 확인.
6. 보고.

한 사이클에 **Test ID 하나**만 해도 된다.

---

## 완료 보고 형식

```
Phase: green | Layer: entity | Track: Logic

## golden
- 경로: tests/golden/t-inc-01.approved.txt
- matched: yes | no

## diff (matched=no 일 때만)
- INT6: …
- ERR: expected … vs actual …

## pytest
- 생성: UPDATE_GOLDEN=1 python -m pytest tests/…::test_…_golden -v → PASSED
- 검증: python -m pytest tests/…::test_…_golden -v → PASSED

## 변경
- tests/_approval.py: assert_matches_golden
- tests/golden/t-inc-01.approved.txt: 생성(UPDATE_GOLDEN)
- tests/test_validate_lines.py: test_…_golden
```

마지막 한 줄 (matched=yes일 때):

```
Golden Master 구축 완료 — 회귀 기준 고정됨
```

---

## 금지 (재확인)

- `tests/golden/*.approved.txt` **수동 편집**으로 matched 통과
- 포맷 임의 변경 (`INT6`/`ERR` 접두어·1-index·ERR 문자열 규칙)
- GREEN 미완료 Test ID에 Golden 연결
- `@pytest.mark.skip`, `xfail`
- UPDATE_GOLDEN 없이 빈 golden으로 테스트 통과시키기

## 다음 단계

- 추가 Test ID Golden 확장: 본 Command 반복
- REFACTOR: 동작 유지하며 `src/` 정리 (golden 재검증 필수)
