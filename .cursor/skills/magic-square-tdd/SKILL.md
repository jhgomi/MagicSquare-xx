---
name: magic-square-tdd
description: >-
  MagicSquare_xx 4×4 마방진 TDD 워크플로(ARRR·Dual-Track·C2C·Command 체인).
  Use when Phase is red, green, or refactor; when running Commands
  /red-test-plan, /red-skeleton, /green-minimal, /refactor-safe; or when the
  user mentions TDD, RED, GREEN, REFACTOR, Dual-Track, C2C, or pytest.fail.
disable-model-invocation: true
---

# magic-square-tdd

MagicSquare_xx **4×4 마방진 10선 검증** TDD Skill. SSOT: `.cursorrules` · `docs/PRD.md`(있으면) · `Report/*.REPORT.md`.

**로드 조건:** 사용자가 Skill·Command를 **명시**했을 때만 적용. 자동 추론으로 워크플로 시작 금지.

---

## 1. ARRR ↔ TDD 매핑

| ARRR | TDD | 단계 | Command 예 |
|------|-----|------|------------|
| **Ask** | **RED** | ③ 설계 | `/red-test-plan` |
| **Ask** | **RED** | ④ 스켈레톤 | `/red-skeleton` |
| **Ask** | **RED** | ⑤ assert | `/tdd-red` |
| **Respond** | **GREEN** | 최소 구현 | `/green-minimal` |
| **Respond** | **GREEN** | 회귀 기준 | `/golden-master` |
| **Refine** | **REFACTOR** | ⑦ 탐지 | `/refactor-smell` |
| **Refine** | **REFACTOR** | safe 적용 | `/refactor-safe` |

한 사이클 = **한 행동** (한 Test ID 또는 RF-xx 1개).

---

## 2. Phase 선언 (응답 첫 줄)

Command·TDD 작업 시 **반드시 첫 줄**:

```
Phase: {red|green|refactor} | Layer: {entity|boundary} | Track: {Logic|UI}
```

| Phase | Layer 기본 | Track 기본 |
|-------|------------|------------|
| `red` | `entity` | `Logic` |
| `green` | `entity` | `Logic` |
| `refactor` | `entity` | `Logic` |

`/refactor-smell`만 예외:

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

`.cursorrules` 단순 TDD: `Phase: RED` | `GREEN` | `REFACTOR` — Command 체인 사용 시 **확장 형식 우선**.

---

## 3. C2C Rule 1~3

| Rule | 계층 | 핵심 |
|------|------|------|
| **Rule1** | Entity | 4×4, `0`=빈칸, 1~16, 마법상수 34, 10선 `R1`~`R4`·`C1`~`C4`·`D1`·`D2` |
| **Rule2** | Control | `validate_lines(grid) -> {"status", "failed_lines"}` |
| **Rule3** | Boundary | incomplete 선행, 대각선 fail, 가짜 완료 fail, 정답 pass |

**완성(pass):** `0` 없음 · 1~16 중복 없음 · 10선 모두 34. **incomplete:** `0` 존재 시 10선 판정 전 종료.

---

## 4. RED 절대 금지

| 금지 | 이유 |
|------|------|
| `src/` 수정·생성 | GREEN 전까지 |
| `@pytest.mark.skip`, `pytest.skip`, `xfail` | RED 무력화 |
| assert 완화·삭제·통과 더미 | 가짜 green |
| Logic Track **Domain Mock** | 실제 `validate_lines` 또는 순수 격자 |
| ECB **E001~E005** emit | 세션 3 범위 밖 |
| GREEN / REFACTOR 선행 | Phase 혼입 |

**RED Then (스켈레톤):** `pytest.fail("RED: {Test ID} — …")` 한 줄만.

**RED Then (완성):** assert로 `status`·`failed_lines` 검증 — **반드시 FAILED**여야 RED 완료.

---

## 5. GREEN 원칙

| 항목 | 규칙 |
|------|------|
| **범위** | `src/`만 (주로 `validate_lines.py`) |
| **1커밋 = 1 RED 묶음** | `/red-test-plan` 블록 3 묶음 단위 |
| **constants SSOT** | `entity/constants.py` — `MAGIC_CONSTANT=34`, `GRID_SIZE=4`, `CELL_MAX=16` |
| **최소 구현** | 현재 RED 테스트 통과에 필요한 코드만 |
| **금지** | 테스트 assert 완화, Solver·GridUI·ECB |

상수 리터럴 `34`/`16`/`4`는 `src/`·`tests/`에서 `entity.constants` import.

---

## 6. REFACTOR 원칙

| 항목 | 규칙 |
|------|------|
| **전제** | `python -m pytest tests/ -v` 전부 PASS |
| **Change Budget** | 파일≤3 · 클래스≤1 · 메서드≤3 |
| **스멜 1개** | `/refactor-safe`는 RF-xx **1개만** |
| **불변** | 입출력·예외·int[6] 1-index·ERR 포맷 |
| **golden** | `UPDATE_GOLDEN` 없이 matched; diff 비의도 → 롤백 |
| **금지** | 기능 추가·버그 수정 (별도 GREEN) |

---

## 7. Track A (UI) vs Track B (Logic)

| | **Track A — UI** | **Track B — Logic** |
|---|------------------|---------------------|
| **Layer** | `boundary` | `entity` |
| **대상** | 입출력·계약·row-major·dict 형식 | `validate_lines`·10선·마법상수 |
| **Mock** | UI Mock만 (세션 3 범위 밖) | **Domain Mock 금지** |
| **ECB** | 후속 세션 | **E001~E005 emit 금지** |
| **테스트** | 경계·직렬화 | 도메인·Control assert |
| **Command** | `Layer: boundary`로 동일 체인 재사용 | 기본 Track |

세션 3 기본 = **Track B (Logic)**.

---

## 8. Command 체인

```
/red-test-plan → /red-skeleton → /tdd-red → /green-minimal → /golden-master
                                                      ↓
                              /refactor-smell → /refactor-safe (반복)
```

| Command | Phase | 산출 | 파일 |
|---------|-------|------|------|
| `/red-test-plan` | red | C2C 표·테스트 플랜 4블록 | 없음 (채팅만) |
| `/red-skeleton` | red | `pytest.fail` 스켈레톤 | `tests/` |
| `/tdd-red` | red | assert 실패 테스트 | `tests/` |
| `/green-minimal` | green | 최소 구현 | `src/` |
| `/golden-master` | green | Approval golden | `tests/golden/` |
| `/refactor-smell` | refactor | 스멜 표·RF 후보 | 없음 (읽기만) |
| `/refactor-safe` | refactor | Safe Refactor 1건 | `src/`·`tests/` |

완료 한 줄 연결:

- test-plan → `/red-skeleton 으로 넘길 준비됐다`
- skeleton → `/tdd-red 으로 넘길 준비됐다`
- smell → `/refactor-safe 에 넘길 후보 준비됐다 — P0 1개를 선택하세요`
- safe → `Safe Refactor 완료 — /refactor-smell 재실행 가능`

---

## 9. pytest 명령 패턴

```bash
# 전체
python -m pytest tests/ -v

# 모듈
python -m pytest tests/test_validate_lines.py -v

# 단일 Test ID
python -m pytest tests/test_validate_lines.py::test_t_inc_01_grid_with_zero -v

# RED 스켈레톤 (FAILED 기대)
python -m pytest tests/test_validate_lines.py::test_d_loc_01_blank_coords_row_major -v

# Golden 생성 (의도적 diff 시만)
UPDATE_GOLDEN=1 python -m pytest tests/ -v -k golden

# Golden 검증 (REFACTOR·일반)
python -m pytest tests/ -v -k golden
```

| Phase | PASS 의미 |
|-------|-----------|
| RED 스켈레톤 | **FAILED** (`pytest.fail`) |
| RED assert (구현 전) | **FAILED** (`AssertionError`) |
| GREEN / REFACTOR | **PASSED** 전부 |

`pythonpath = ["src"]` — `pyproject.toml` 기준.

---

## 10. 완료 보고 형식

### RED (test-plan)

```
Phase: red | Layer: entity | Track: Logic
[블록 1 C2C] [블록 2 Track B] [블록 3 플랜] [블록 4 ECB]
/red-skeleton 으로 넘길 준비됐다
```

### RED (skeleton)

```
Phase: red | Layer: entity | Track: Logic
## 변경 (tests/만)
## pytest — Test ID · FAIL 한 줄
/tdd-red 으로 넘길 준비됐다
```

### RED (tdd-red)

```
Phase: RED
## 변경 · Arrange · Assert
## pytest — FAILED
## 다음 — GREEN
```

### GREEN (minimal)

```
Phase: green | Layer: entity | Track: Logic
## 변경 (src/)
## pytest — PASSED
```

### Golden

```
Phase: green | Layer: entity | Track: Logic
## golden — 경로 · matched
```

### REFACTOR (smell)

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
## pytest 전제 · 스멜 표 · RF 후보
/refactor-safe 에 넘길 후보 준비됐다 — P0 1개를 선택하세요
```

### REFACTOR (safe)

```
Phase: refactor | Layer: entity | Track: Logic
## 대상 RF-xx · 변경 요약 · Budget
## pytest · golden matched
Safe Refactor 완료 — /refactor-smell 재실행 가능
```

---

## 부록 — 핵심 경로·픽스처

| 경로 | 역할 |
|------|------|
| `src/validate_lines.py` | Control 진입점 |
| `entity/constants.py` | 상수 SSOT |
| `tests/test_validate_lines.py` | Logic 테스트 |
| `tests/conftest.py` | `grid_g1` (row-major, `0`×2) |
| `tests/_approval.py` | `assert_matches_golden` |
| `tests/golden/{id}.approved.txt` | Golden 기준 |

### Golden 포맷 (고정)

```
INT6 <6정수 1-index>
ERR status={pass|fail|incomplete} failed={축ID목록|none}
```

### RED 우선 Test ID (기본)

| Test ID | Then |
|---------|------|
| T-INC-01 | `incomplete`, `failed_lines []` |
| T-FAIL-D1 | `fail`, `"D1"` ∈ `failed_lines` |
| T-FAIL-FAKE | 행·열만 34 → `fail` |
| T-PASS-01 | `pass`, `failed_lines []` |

---

## 금지 요약

- RED: `src/`, skip, xfail, assert 완화, Domain Mock, ECB emit
- GREEN: 테스트 완화, 범위 밖 Solver/UI
- REFACTOR: Budget 초과, 스멜 2개+, golden 수동 편집, 기능 변경
- 공통: git commit은 **사용자 요청 시만** · 대화 **한국어**

## Command 상세

`.cursor/commands/{red-test-plan,red-skeleton,tdd-red,green-minimal,golden-master,refactor-smell,refactor-safe}.md`
