# MagicSquare_xx — Product Requirements Document (PRD)

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_xx / MagicSquare_1004 |
| **버전** | 0.1 (세션 3 — 10선 검증) |
| **작성일** | 2026-06-10 |
| **SSOT** | 본 문서 · `.cursorrules` · `Report/01`~`04` |
| **현재 범위** | `validate_lines` Control · TDD Test Loop |

---

## 1. 개요

### 1.1 한 줄 요약

**4×4 마방진에서 행·열·양 대각선(10선)이 모두 34인지 판정하는 검증 규칙과 확인 루프** — 대각선 누락으로 “맞췄다”고 착각해 20분을 쓰는 일을 줄이기 위함.

### 1.2 배경

4×4 마방진 과제에서 학습자는 빈칸 2개를 채우고 1~16 숫자를 배치하며 행·열·대각선 합 34를 맞춘다. Mom Test 인터뷰에서 **대각선 1축 검증 누락**으로 잘못 완료한 뒤 **20분** 재작업했고, 오류는 **제출·채점 후**에야 발견되었다.

### 1.3 증거 3줄 (Mom Test)

1. 「빈칸 2개 넣고 행·열·대각선 합 맞췄는데」
2. 「대각선 하나를 빼먹어서」
3. 「20분 날렸다」

---

## 2. 페르소나·문제

### 2.1 페르소나 (Role)

4×4 격자, 빈칸 2개(`0`), 1~16, 합 34를 맞추는 **학습자** (손으로/코드로 다룸). 검증 누락 → 채점 후 20분 손실을 겪은 당사자.

### 2.2 진짜 문제

4×4 마방진에서 빈칸 2개와 합 34를 맞추다 **행·열·대각선(10선)을 모두 검증하지 못해** 잘못 완료한 뒤 20분을 썼고, 틀림은 제출·채점 후에야 알았다.

### 2.3 표면 문제 (비목표)

- 「4×4 마방진 ECB 구조로 **프로그램(솔버·UI) 만든다**」
- 「빈칸 2개 찾아 채우는 **마방진 앱·과제**를 완성한다」

→ 솔루션명이 섞인 정의. 본 PRD 목표가 **아님**.

---

## 3. R-G-I-O

| | 내용 |
|---|------|
| **Role** | §2.1 페르소나 |
| **Goal** | 채운 격자가 **10축 합 34** + **0 없음** + **1~16 중복 없음**을 **제출 전에** 한 번에 판정하고, 틀리면 **어느 축**이 깨졌는지 알 수 있게 한다 |
| **Input** | 4×4 정수 격자 — 중첩 `list[list[int]]` 또는 flat 16 (테스트에서 명시). `0`=빈칸, `1~16`=채운 값 |
| **Output** | `{"status": "pass" \| "fail" \| "incomplete", "failed_lines": list[str]}` — fail 시 깨진 축 ID (`R1`~`R4`, `C1`~`C4`, `D1`, `D2`) |

---

## 4. 성공 기준

| # | 기준 | Mom Test 연결 |
|---|------|---------------|
| SC-1 | **10축 + 숫자 규칙**을 빠짐없이 검사한다 | 증거 1 — 대각선 포함 전 축 |
| SC-2 | 임의 축 하나만 34가 아니거나 **F3(숫자 규칙) 위반**이면 **fail** — “완료” 금지 | 증거 2 — 부분 검증 통과 금지 |
| SC-3 | fail 시 **어느 축이 틀렸는지** `failed_lines`로 제공 — 채점 후 20분 재작업 방지 | 증거 3 — 제출 전 판정 |

---

## 5. 기능 요구사항 (FR)

### 5.1 Entity (도메인)

| ID | 요구 | 상세 |
|----|------|------|
| **FR-1** | 4×4 격자 | 정수 리스트(또는 중첩 리스트). 크기·형식 불일치 시 검증 대상 아님 |
| **FR-2** | 셀 값 규칙 | `0`=빈칸. 완성 시 `1~16`만, **중복 없음**. 범위 밖·음수 invalid |
| **FR-3** | 마법상수 34 | 행 4 + 열 4 + 주대각 `D1` + 부대각 `D2` = **10선** 각 합 34 |
| **FR-4** | 10선 축 ID | `R1`~`R4`, `C1`~`C4`, `D1`, `D2` — `LINE_IDS` 고정 |
| **FR-5** | incomplete 선행 | `0`이 하나라도 있으면 10선 판정 **전** `incomplete`. 행·열만 맞아도 pass 금지 |
| **FR-6** | pass 조건 | `0` 없음 · 1~16 중복 없음 · 10선 모두 34 — **동시** 만족 |

### 5.2 Control (검증 API)

| ID | 요구 | 상세 |
|----|------|------|
| **FR-7** | 진입점 | `validate_lines(grid) -> dict` (`src/validate_lines.py`) |
| **FR-8** | status | `pass` \| `fail` \| `incomplete` (정의见 §6) |
| **FR-9** | failed_lines | fail 시 깨진 축 ID 목록. **pass·incomplete 시 `[]`** |
| **FR-10** | ECB 분리 | Control은 Entity만 해석. UI·입력 형식 변환·이벤트 emit 없음 |

### 5.3 Boundary (입출력·테스트)

| ID | 요구 | 상세 |
|----|------|------|
| **FR-11** | 입력 형식 | 4×4 중첩 또는 flat 16 — 테스트에서 명시 |
| **FR-12** | 출력 계약 | dict만. CLI·GridUI·사람용 메시지는 후속 세션 |
| **FR-13** | 상수 SSOT | `entity/constants.py` — `MAGIC_CONSTANT=34`, `GRID_SIZE=4`, `CELL_MAX=16` |
| **FR-14** | Golden Master | GREEN PASS 후 `tests/golden/{id}.approved.txt` — `INT6` + `ERR` 포맷 |

### 5.4 실패 조건 (Mom Test → ECB)

| ID | 조건 | 대응 |
|----|------|------|
| **F1** | 10선 중 일부 합 ≠ 34인데 “완료” 처리 | `validate_lines` → `fail` |
| **F2** | 빈칸 ≠ 2개 또는 위치 오류 | 후속 `MissingFinder` (본 세션 범위 밖) |
| **F3** | 1~16 중복·누락·`0` 잔존 (완성 시) | `validate_lines` → `fail` |
| **F4** | 실패 시 어느 축이 틀렸는지 미제공 | `failed_lines` 필수 |

---

## 6. API 계약 — `validate_lines`

### 6.1 시그니처

```python
def validate_lines(grid: list) -> dict:
    """4×4 격자 10선 검증."""
```

### 6.2 반환

```python
{"status": "pass" | "fail" | "incomplete", "failed_lines": list[str]}
```

| status | 조건 | failed_lines |
|--------|------|--------------|
| `incomplete` | `0`(빈칸) 존재 또는 완성 판정 불가 | `[]` |
| `fail` | 완성 격자이나 10선 중 합 ≠ 34 **또는** F3 위반 | 깨진 축 ID (예 `["D1", "R2"]`) |
| `pass` | FR-6 전부 만족 | `[]` |

### 6.3 상수·축 ID

```python
MAGIC_CONSTANT = 34
LINE_IDS = ["R1","R2","R3","R4","C1","C2","C3","C4","D1","D2"]
```

---

## 7. 비범위 (Out of Scope — 세션 3)

| 항목 | 사유 |
|------|------|
| 빈칸 2개 **자동 풀이·Solver** | 진짜 문제는 검증 누락 |
| **ECB 전체** · **GridUI / 앱** | 검증·루프 우선 |
| 행·열만 34인 **불완전 검증** | 증거 2 직접 원인 |
| 채점·제출 **시스템 연동** | 로컬 검증 루프만 |
| ECB **E001~E005** emit | 후속 세션 |
| `validate_axis` · `report_failures` | 선택·보조 (후속) |

---

## 8. 테스트 요구사항

### 8.1 RED 우선 케이스

| Test ID | FR | Given | Then |
|---------|-----|-------|------|
| **T-INC-01** | FR-5 | `0` 포함 4×4 | `status=="incomplete"`, `failed_lines==[]` |
| **T-FAIL-D1** | FR-3,7 | 행·열 34, 대각선만 틀림 | `status=="fail"`, `"D1"` ∈ `failed_lines` |
| **T-FAIL-FAKE** | FR-3,6 | 행·열만 34 (가짜 완료) | `status=="fail"` (pass 금지) |
| **T-PASS-01** | FR-6,7 | 정답 4×4 마방진 | `status=="pass"`, `failed_lines==[]` |

### 8.2 픽스처

| 이름 | 설명 |
|------|------|
| `grid_g1` | row-major flat 16, `0` **정확히 2개** (`tests/conftest.py`) |

### 8.3 Golden 포맷

```
INT6 <6정수 1-index>
ERR status={pass|fail|incomplete} failed={축ID목록|none}
```

### 8.4 TDD 규칙

- 순서: **RED → GREEN → REFACTOR**. 한 사이클에 한 행동.
- RED: `tests/`만. GREEN: `src/`만.
- 금지: assert 완화, skip, xfail, RED 단계 `src/` 선행 수정.

---

## 9. 개발 워크플로 (ARRR · Dual-Track)

### 9.1 ARRR ↔ TDD

| ARRR | TDD | Command |
|------|-----|---------|
| Ask | RED | `/red-test-plan` → `/red-skeleton` → `/tdd-red` |
| Respond | GREEN | `/green-minimal` → `/golden-master` |
| Refine | REFACTOR | `/refactor-smell` → `/refactor-safe` |

### 9.2 Dual-Track

| Track | Layer | 세션 3 |
|-------|-------|--------|
| **B — Logic** | `entity` | **기본** — `validate_lines`, 10선 |
| **A — UI** | `boundary` | 후속 — row-major, dict 계약 |

Logic Track: **Domain Mock 금지**. ECB emit 금지.

### 9.3 C2C Rule

| Rule | 계층 |
|------|------|
| Rule1 | Entity — FR-1~6 |
| Rule2 | Control — FR-7~10 |
| Rule3 | Boundary — FR-11~14, RED 케이스 |

### 9.4 REFACTOR Budget

파일 ≤ 3 · 클래스 ≤ 1 · 메서드 ≤ 3 · 스멜 1개/사이클.

---

## 10. 기술 스택·구조

```
MagicSquare_xx/
├── docs/
│   └── PRD.md                 # 본 문서
├── src/
│   └── validate_lines.py      # Control (FR-7)
├── entity/
│   └── constants.py           # FR-13 (예정)
├── tests/
│   ├── test_validate_lines.py
│   ├── conftest.py            # grid_g1
│   ├── _approval.py           # Golden (예정)
│   └── golden/                # *.approved.txt (예정)
├── Report/                    # 세션 보고서
├── Prompting/                 # Transcript
├── .cursorrules               # Entity·Control·Boundary 요약
├── .cursor/commands/          # TDD·Refactor Commands
└── .cursor/skills/
    ├── magic-square-tdd/
    └── magic-square-docs/
```

| 항목 | 값 |
|------|-----|
| **언어** | Python 3 |
| **테스트** | pytest (`pyproject.toml`: `testpaths=["tests"]`, `pythonpath=["src"]`) |
| **아키텍처** | ECB — 세션 3은 Control(`validate_lines`)만 구현 |

---

## 11. Test Loop

```
[격자 입력] → validate_lines → pass? → 종료(완료 인정)
                    ↓ fail / incomplete
              실패 축 확인 → 격자 수정 → validate_lines (반복)
```

| 단계 | 케이스 |
|------|--------|
| Red | 대각선만 틀림 → fail (증거 2) |
| Green | 정답 격자 → pass (증거 1) |
| 회귀 | 행·열만 34 가짜 완료 → fail (증거 3) |

---

## 12. 로드맵

| 단계 | 내용 | 상태 |
|------|------|------|
| STEP 1 | Mom Test — 문제 정의 | ✅ |
| STEP 2 | Mom Test 질문 세트 | ✅ |
| STEP 3 | 워크북 · `validate_lines` 계약 · TDD | 🔄 진행 중 |
| STEP 4 | `validate_lines` GREEN 구현 | ⏳ |
| STEP 5 | Golden Master · REFACTOR | ⏳ |
| 후속 | `MissingFinder`, `Solver`, GridUI, ECB | ⏳ 범위 밖 |

---

## 13. 참고 문서

| 문서 | 내용 |
|------|------|
| [Report/01.REPORT.md](../Report/01.REPORT.md) | Mom Test 인터뷰 |
| [Report/02.REPORT.md](../Report/02.REPORT.md) | Mom Test 질문 10개 |
| [Report/03.REPORT.md](../Report/03.REPORT.md) | 세션 3 워크북 |
| [Report/04.REPORT.md](../Report/04.REPORT.md) | R-G-I-O vs `validate_lines` 리뷰 |
| `.cursorrules` | Entity·Control·Boundary·TDD 요약 |

---

## 14. 변경 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 0.1 | 2026-06-10 | 초안 — Report 01~04·`.cursorrules`·Skills·Commands 통합. FR-1~14, F1~F4, API 계약, Test ID 확정 |
