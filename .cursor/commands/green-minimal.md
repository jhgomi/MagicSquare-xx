# green-minimal

ARRR **R단계 (Respond = GREEN)** — `/red-test-plan` **RED 묶음 1개**당 **`src/` 최소 구현**만 수행한다. **1커밋 = 1 RED 묶음.**

**magic-square-tdd Skill이 있으면 자동 따름** (상수 SSOT·ECB·최소 구현 원칙 우선).

SSOT: 직전 `/red-test-plan` 블록 3 · `/tdd-red` assert · `.cursorrules` · `docs/PRD.md`(있으면)

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: green | Layer: entity | Track: Logic
```

| 항목 | 값 | 기본 |
|------|-----|------|
| **Phase** | `green` | 고정 (RED·REFACTOR 금지) |
| **Layer** | `entity` \| `boundary` | `/red-test-plan`과 동일 |
| **Track** | `Logic` \| `UI` | `/red-test-plan`과 동일 |

**Track A (boundary):** `Layer: boundary`만 바꾸면 본 Command를 **그대로 재사용**한다.

---

## 선행 조건

| 항목 | 요구 |
|------|------|
| **RED 묶음** | `/red-test-plan` 블록 3에 정의된 Test ID **1묶음**만 대상 |
| **테스트** | 해당 ID 테스트 존재 (`pytest.fail` 또는 assert) |
| **실패 상태** | 구현 전: 대상 테스트 **FAILED** (RED 완료) |

채팅에 RED 묶음이 없으면 SSOT(`.cursorrules`·`Report/03`)·`tests/test_*.py`에서 **이번 GREEN 대상 Test ID를 자동 추출**한다. 사용자에게 Test ID 재질문 금지.

---

## 작업 절차

1. **RED 재확인** — 이번 RED 묶음 Test ID·Given/When/Then·기대 `status`·`failed_lines`를 설계표·테스트에서 확인.
2. **`src/` 최소 구현** — 대상 Test ID를 **PASS**시키는 **최소 코드**만 `src/`(주로 `validate_lines.py`)에 추가·수정.
3. **`pytest.fail` 제거 · assert 교체** — RED 묶음 테스트에 `pytest.fail`이 남아 있으면 `/tdd-red` 설계대로 **assert 본문**으로 교체. 이미 assert면 **테스트 수정 금지**.
4. **PASS 확인** — pytest 실행. 대상 Test ID **PASSED**. 회귀(다른 테스트 FAIL) 시 **즉시 수정** 후 재실행.

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `src/` — 최소 구현 (`validate_lines.py` 등) | 이번 RED 묶음 **외** Test ID 동시 해결 |
| `tests/` — **`pytest.fail` → assert 교체만** (해당 ID) | assert 완화·삭제·기대값 축소 |
| `entity/constants.py` — 상수 **참조** (`from entity.constants import …`) | 상수 **값** 변경·중복 정의 |
| | REFACTOR (구조 개선·리네임·추출) |
| | Solver · GridUI · ECB emit |
| | `@pytest.mark.skip`, `pytest.skip`, `xfail` |
| | git commit (사용자 요청 시만) |

---

## 상수 SSOT — 하드코딩·매직넘버 금지

`34` · `16` · `4` 리터럴을 `src/`·`tests/` 본문에 **직접 쓰지 않는다**. SSOT:

```python
# entity/constants.py
MAGIC_CONSTANT = 34
GRID_SIZE = 4
CELL_MAX = 16
```

```python
# src/validate_lines.py (예)
from entity.constants import MAGIC_CONSTANT, GRID_SIZE, CELL_MAX
```

| 금지 | 허용 |
|------|------|
| `src/`에 `MAGIC_CONSTANT = 34` 중복 정의 | `entity.constants` import |
| 테스트·구현 본문 리터럴 `34`/`16`/`4` | 상수 import 후 사용 |
| 설계에 없는 임의 상수 추가 | 필요 시 `entity/constants.py`에 **한 곳**만 정의 |

---

## ECB · E001~E005

| 규칙 | 내용 |
|------|------|
| **E001~E005** | `raise` · `return` · emit **금지** — 세션 3 범위 밖 |
| **Entity 계층** | `boundary` · `control` 패키지 **import 금지** |
| **Control** | Entity 규칙만 해석 — UI·입력 변환·이벤트 없음 |
| **반환 계약** | `validate_lines(grid) -> {"status", "failed_lines"}` 고정 |

---

## GREEN 최소 구현 원칙

- **한 사이클 = RED 묶음 1개 = Test ID 1~N개**(블록 3 범위 내)만 통과시키는 코드.
- **미래 Test ID**를 미리 구현하지 않는다 (YAGNI).
- **incomplete** 판정: `0` 존재 시 10선 판정 **전** 종료 (`.cursorrules`).
- **fail** 판정: 완성 격자에서 깨진 축 ID를 `failed_lines`에 포함.
- **pass** 판정: `0` 없음 · 1~16 중복 없음 · 10선 모두 `MAGIC_CONSTANT`.

### 구현 스텁 예 — incomplete (T-INC-01)

```python
from entity.constants import GRID_SIZE, MAGIC_CONSTANT


def validate_lines(grid: list) -> dict:
    flat = [cell for row in grid for cell in row]
    if 0 in flat:
        return {"status": "incomplete", "failed_lines": []}
    # … 이후 RED 묶음 범위 밖 — 다음 GREEN에서
    return {"status": "fail", "failed_lines": []}
```

---

## assert 교체 (pytest.fail 잔존 시)

`/tdd-red` 미실행·스켈레톤만 있을 때 **해당 Test ID Then**만 교체:

```python
# Before (RED 스켈레톤)
pytest.fail("RED: T-INC-01 — expect status incomplete, failed_lines []")

# After (GREEN — assert)
assert result["status"] == "incomplete"
assert result["failed_lines"] == []
```

- **Then**에 assert만 — `pytest.fail`·`pass`·통과 더미 금지.
- assert 내용은 `/red-test-plan`·설계표 Then과 **동일** (완화 금지).

---

## pytest 실행

단일 Test ID:

```bash
python -m pytest tests/test_validate_lines.py::test_t_inc_01_grid_with_zero -v
```

파일 전체 (회귀 확인):

```bash
python -m pytest tests/test_validate_lines.py -v
```

**성공 기준:**

| 대상 | 기대 |
|------|------|
| 이번 RED 묶음 Test ID | **PASSED** |
| 기존 GREEN 테스트 | **PASSED** (회귀 없음) |
| 아직 RED인 테스트 | FAILED 허용 (다음 사이클) |

회귀 FAIL 발생 시 GREEN 완료 보고 **전에** 반드시 수정·재실행.

`pythonpath = ["src"]` — `pyproject.toml` 기준.

---

## 1커밋 = 1 RED 묶음

| 항목 | 규칙 |
|------|------|
| **커밋 단위** | RED 묶음 1개 GREEN 완료 = 커밋 1개 (사용자 요청 시) |
| **범위** | 해당 묶음 `src/` 변경 + (필요 시) assert 교체 |
| **메시지 예** | `feat(green): T-INC-01 incomplete 판정` |

git commit은 **사용자가 명시적으로 요청할 때만** 수행.

---

## 완료 보고 형식

작업 후 **pytest를 실행**하고 아래를 반드시 보고한다:

1. **PASS Test ID** — 이번 GREEN으로 통과한 ID
2. **변경 파일** — `src/`(및 assert 교체 시 `tests/`) 목록
3. **회귀** — 다른 테스트 FAIL 시 수정 내역; 없으면 `회귀 없음`

```
Phase: green | Layer: entity | Track: Logic

## PASS Test ID
- T-INC-01

## 변경
- src/validate_lines.py: 0 포함 시 incomplete 반환
- tests/test_validate_lines.py: T-INC-01 pytest.fail → assert (해당 시만)

## pytest
- 단일: python -m pytest tests/test_validate_lines.py::test_t_inc_01_grid_with_zero -v
- 전체: python -m pytest tests/test_validate_lines.py -v
- T-INC-01 · PASSED
- 회귀: 없음 (또는 수정 후 PASSED)

## 다음
- /golden-master: T-INC-01 Golden 구축 (선택)
- 다음 RED 묶음: T-FAIL-D1
```

마지막 한 줄 (대상 Test ID PASS · 회귀 없음):

```
/golden-master 또는 다음 RED 묶음 GREEN 준비됐다
```

---

## 금지 (재확인)

- 이번 RED 묶음 **외** Test ID 동시 해결 (선행 구현·일괄 pass)
- REFACTOR — 구조 개선은 `/refactor-smell` → `/refactor-safe`
- assert 완화 · `@pytest.mark.skip` · `pytest.skip` · `xfail`
- `34`/`16`/`4` 리터럴 — `entity.constants` import 필수
- E001~E005 `raise`/`return`/emit
- Entity에서 boundary/control import
- Solver · GridUI · ECB UI
- git commit (사용자 요청 시만)
- pytest FAIL·회귀 상태에서 완료 보고

## 다음 단계

- 회귀 기준: `/golden-master` (해당 Test ID PASS 후)
- 구조 개선: `/refactor-smell` → `/refactor-safe` (전 테스트 PASS 전제)
- 다음 기능: RED 묶음 1개씩 `/green-minimal` 반복
