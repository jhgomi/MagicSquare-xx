# MagicSquare_xx

4×4 마방진 **10선(행·열·대각선) 검증** — 대각선 누락으로 “맞췄다”고 착각해 20분을 쓰는 일을 줄이기 위한 로컬 검증 루프.

| 항목 | 내용 |
|------|------|
| **버전** | 0.1 (세션 3) |
| **PRD** | [docs/PRD.md](docs/PRD.md) |
| **계약** | `.cursorrules` |

---

## 문제 (Mom Test)

4×4 마방진에서 빈칸 2개와 합 34를 맞추다 **행·열·대각선을 모두 검증하지 못해** 잘못 완료한 뒤 20분을 썼고, 틀림은 **제출·채점 후**에야 알았다.

**이번 세션 목표:** `validate_lines`로 10선을 제출 전에 판정하고, fail 시 **어느 축**이 깨졌는지 반환한다.

**비목표:** Solver, GridUI, ECB 앱, 채점 시스템 연동.

---

## 빠른 시작

### 요구 사항

- Python 3
- pytest

### 설치·실행

```bash
# 저장소 루트에서
python -m pytest tests/ -v
```

`pyproject.toml`에 `pythonpath = ["src"]`가 설정되어 있다.

---

## API

```python
from validate_lines import validate_lines

result = validate_lines(grid)  # 4×4 list[list[int]]
# {"status": "pass" | "fail" | "incomplete", "failed_lines": [...]}
```

| status | 의미 | failed_lines |
|--------|------|--------------|
| `incomplete` | `0`(빈칸) 존재 — 10선 판정 전 종료 | `[]` |
| `fail` | 10선 중 합 ≠ 34 또는 숫자 규칙 위반 | 깨진 축 ID |
| `pass` | `0` 없음 · 1~16 중복 없음 · 10선 모두 34 | `[]` |

**10선 축 ID:** `R1`~`R4`, `C1`~`C4`, `D1`(주대각), `D2`(부대각)  
**마법상수:** 34

상세: [docs/PRD.md §6](docs/PRD.md#6-api-계약--validate_lines)

---

## 프로젝트 구조

```
MagicSquare_xx/
├── docs/PRD.md              # 요구사항 SSOT
├── src/validate_lines.py    # Control — 10선 검증
├── tests/                   # pytest
├── Report/                  # 세션 보고서
├── Prompting/               # 대화 Transcript
├── .cursorrules             # Entity·Control·Boundary
├── .cursor/commands/        # TDD·Refactor Commands
└── .cursor/skills/          # magic-square-tdd, magic-square-docs
```

---

## TDD 워크플로

```
RED → GREEN → REFACTOR
```

| Phase | 범위 | Command 예 |
|-------|------|------------|
| RED | `tests/` | `/red-test-plan` → `/red-skeleton` → `/tdd-red` |
| GREEN | `src/` | `/green-minimal` → `/golden-master` |
| REFACTOR | 구조만 | `/refactor-smell` → `/refactor-safe` |

한 사이클에 **한 행동**. RED에서 `src/` 수정 금지.

Skills: `.cursor/skills/magic-square-tdd/`, `.cursor/skills/magic-square-docs/`

---

## RED 우선 테스트

| Test ID | 기대 |
|---------|------|
| T-INC-01 | `incomplete`, `failed_lines == []` |
| T-FAIL-D1 | `fail`, `"D1"` ∈ `failed_lines` |
| T-FAIL-FAKE | 행·열만 34 → `fail` |
| T-PASS-01 | `pass`, `failed_lines == []` |

```bash
python -m pytest tests/test_validate_lines.py -v
```

---

## Test Loop

```
[격자 입력] → validate_lines → pass? → 완료
                    ↓ fail / incomplete
              failed_lines 확인 → 수정 → 재검증
```

---

## 문서

| NN | Report | Transcript | 주제 | 날짜 |
|----|--------|------------|------|------|
| 01 | [01.REPORT.md](Report/01.REPORT.md) | [01.REPORT.md](Prompting/01.REPORT.md) | Mom Test 인터뷰 | 2026-06-10 |
| 02 | [02.REPORT.md](Report/02.REPORT.md) | [02.REPORT.md](Prompting/02.REPORT.md) | Mom Test 질문 10개 | 2026-06-10 |
| 03 | [03.REPORT.md](Report/03.REPORT.md) | [03.REPORT.md](Prompting/03.REPORT.md) | 세션 3 워크북 | 2026-06-10 |
| 04 | [04.REPORT.md](Report/04.REPORT.md) | [04.REPORT.md](Prompting/04.REPORT.md) | R-G-I-O vs validate_lines | 2026-06-10 |
| 05 | [05.REPORT.md](Report/05.REPORT.md) | [05.Export-Transcript.md](Prompting/05.Export-Transcript.md) | TDD Command·Skill·PRD·README | 2026-06-10 |

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](docs/PRD.md) | FR-1~14, API, Test ID, 로드맵 |
| [.cursorrules](.cursorrules) | Entity·Control·Boundary·TDD 요약 |

Export: `/export` · `/export-session` → `magic-square-docs` Skill

---

## 로드맵

| 단계 | 상태 |
|------|------|
| STEP 1~2 Mom Test | ✅ |
| STEP 3 `validate_lines` 계약·TDD | 🔄 |
| GREEN 구현 · Golden · REFACTOR | ⏳ |
| Solver · GridUI · ECB | ⏳ 후속 |

---

## 라이선스·기여

교육용 프로젝트 (MagicSquare_1004). 기여·커밋 정책은 세션 가이드(`.cursorrules`)를 따른다.
