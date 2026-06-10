# red-test-plan

ARRR **A단계 (Ask = RED ③)** — C2C 설계표·테스트 플랜만 작성한다. **코드·테스트 파일은 만들지 않는다.**

SSOT: `.cursorrules` · `docs/PRD.md`(있으면) · 채팅 맥락 · `Report/*.REPORT.md`

## 동작 조건

- **추가 입력 없이** `/red-test-plan` 만으로 실행한다.
- **세션 주제**·**Test ID**는 채팅·PRD·`.cursorrules`에서 **자동 추출**한다. 사용자에게 되묻지 않는다.
- PRD가 없으면 `.cursorrules` Entity·Control·Boundary + `Report/03.REPORT.md` 성공 기준을 FR 대용으로 쓴다.

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 3항을 한 줄로:

```
Phase: red | Layer: entity | Track: Logic
```

| 항목 | 값 | 기본 |
|------|-----|------|
| **Phase** | `red` | 고정 (GREEN·REFACTOR 금지) |
| **Layer** | `entity` \| `boundary` | Logic Track → `entity` (Control·도메인 검증) |
| **Track** | `Logic` \| `UI` | 세션 3 기본 → `Logic` |

**Track A (boundary):** UI·입출력·계약 경계 테스트일 때 `Layer: boundary`만 바꾸면 본 Command를 **그대로 재사용**한다. Track·출력 4블록 형식은 동일.

---

## 수정·생성 범위

| 허용 | 금지 |
|------|------|
| 채팅에 C2C 표·테스트 플랜 **텍스트 출력** | `tests/` · `src/` **파일 생성·수정** |
| PRD FR·Rule 인용 | GREEN / REFACTOR 단계 진입 |
| Test ID·Given/When/Then 설계 | `@pytest.mark.skip`, `xfail`, assert 완화 전제 |
| | Domain Mock (Logic Track) |
| | ECB E001~E005 emit·UI 이벤트 설계 |
| | git commit (사용자 요청 시만) |

---

## C2C Rule (설계표 작성 규칙)

| Rule | 의미 | 설계 시 확인 |
|------|------|----------------|
| **Rule1** | **Entity** — 4×4, 0=빈칸, 1~16, 마법상수 34, 10선 ID | 격자·축 ID가 Rule과 일치하는가 |
| **Rule2** | **Control** — `validate_lines(grid) -> dict` 계약 | `status` 3값, `failed_lines` 규칙 |
| **Rule3** | **Boundary** — RED 우선 케이스·입력 형식 | incomplete 선행, 대각선 fail, 가짜 완료 fail, pass |

한 Test ID = **To-Do 1개** = **한 행동·한 검증** (TDD 한 사이클).

---

## 출력 4블록 (표 형식, 순서 고정)

아래 4블록을 **모두** 채워 응답한다. 표는 마크다운 테이블.

### 블록 1 — C2C (Rule1~3)

PRD **FR** (또는 `.cursorrules` / 성공 기준) 인용 → **To-Do 1개** → **Test ID** + Given / When / Then.

| Rule | PRD FR (인용) | To-Do (1개) | Test ID | Given | When | Then |
|------|---------------|-------------|---------|-------|------|------|
| Rule1 | FR-…: «…» | … | T-… | … | … | … |
| Rule2 | FR-…: «…» | … | T-… | … | … | … |
| Rule3 | FR-…: «…» | … | T-… | … | … | … |

- **Given:** 4×4 격자(중첩 `list[list[int]]`)·상수; `0`=빈칸.
- **When:** `result = validate_lines(grid)` (또는 boundary 대상 함수).
- **Then:** `result["status"]`, `result["failed_lines"]` 기대값 (`R1`~`R4`, `C1`~`C4`, `D1`, `D2`).

**세션 3 RED 우선 Test ID (Logic·entity, SSOT 기본):**

| Test ID | Rule | Then 요약 |
|---------|------|-----------|
| T-INC-01 | Rule3 | `status == "incomplete"`, `failed_lines == []` |
| T-FAIL-D1 | Rule1·2 | `status == "fail"`, `"D1"` ∈ `failed_lines` |
| T-FAIL-FAKE | Rule1·3 | 행·열만 34 → `status == "fail"` (pass 금지) |
| T-PASS-01 | Rule1·2 | `status == "pass"`, `failed_lines == []` |

채팅·PRD에 이미 정의된 Test ID가 있으면 위 기본값 대신 **그 ID를 우선**한다.

### 블록 2 — Track B (상세 명세)

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|---------------------|
| T-… | `validate_lines` | … | … | … |

- **Invariant:** RED 전후에도 깨지면 안 되는 계약 (예: pass/incomplete 시 `failed_lines == []`, fail 시 축 ID만 포함).
- **Expected RED Failure:** 구현 전 pytest가 **실패해야 하는 이유** 한 줄 (예: `NotImplementedError`, `AssertionError: status 'pass' != 'fail'`, 스텁 `...`).

### 블록 3 — 테스트 플랜

| 항목 | 내용 |
|------|------|
| **파일 경로** | `tests/test_validate_lines.py` (boundary면 해당 모듈) |
| **함수명** | `test_<snake_case>` — Test ID와 1:1 매핑 |
| **conftest 픽스처** | 필요 시만: `complete_grid`, `grid_with_zero`, `diagonal_only_wrong` 등 — **이 단계에서는 이름·역할만 기술**, 파일 생성 안 함 |
| **pytest 명령** | `python -m pytest tests/test_validate_lines.py -v` |
| **RED 묶음 범위** | 이번 사이클에 `/red-skeleton`·`/tdd-red`로 넘길 Test ID 목록 (예: `T-INC-01` 단독 또는 `T-FAIL-D1`~`T-FAIL-FAKE`) |

### 블록 4 — ECB·Mock 점검

| 점검 항목 | Logic Track | UI Track |
|-----------|-------------|----------|
| Domain Mock | **금지** — `validate_lines` 실제 호출 또는 순수 입력 격자 | UI Mock만 허용 (본 세션 범위 밖) |
| ECB emit E001~E005 | **금지** — 이벤트·GridUI·Solver 없음 | 해당 시만 점검 |
| Solver / GridUI | 범위 밖 | 범위 밖 |
| pass/incomplete 시 `failed_lines` | `[]` 유지 | 동일 |
| incomplete 선행 | `0` 있으면 10선 판정 전 `incomplete` | 동일 |

Logic Track이면 블록 4 마지막 줄에 반드시:

```
✓ Domain Mock 없음 · E001~E005 emit 없음 · ECB/UI 범위 밖
```

---

## 자동 추출 가이드 (에이전트용)

1. **세션 주제:** `.cursorrules` 첫 줄 또는 PRD 한 줄 요약 (예: «4×4 마방진 10선 검증»).
2. **Layer:** `validate_lines`·10선·마법상수 → `entity`; flat 16·dict 계약·pytest 경계 → `boundary` 후보. 기본 `entity`.
3. **Track:** Solver·GridUI·ECB 언급 없으면 `Logic`.
4. **FR 인용:** PRD `FR-n` 없으면 `Report/03` 성공 기준 1~3 또는 `.cursorrules` 해당 절을 «…»로 인용.
5. **Test ID:** 채팅에已有 ID → 유지; 없으면 블록 1 기본 ID 또는 `T-<RULE>-<nn>`.

---

## 완료 보고 (마지막 한 줄)

4블록 출력 후 **반드시** 마지막 줄:

```
/red-skeleton 으로 넘길 준비됐다
```

---

## 금지 (재확인)

- `src/` · `tests/` **파일 생성·수정**
- GREEN / REFACTOR / `validate_lines` 본문 구현
- `@pytest.mark.skip`, `pytest.skip`, `xfail`
- Logic Track에서 Domain·Control Mock
- ECB E001~E005 및 GridUI 설계
- 사용자에게 세션 주제·Test ID **재질문** (SSOT·채팅에서 추출)

## 다음 단계

- 테스트 **골격·파일** 작성: `/red-skeleton`
- RED **실패 테스트** 작성: `/tdd-red`
