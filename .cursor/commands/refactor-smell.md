# refactor-smell

ARRR **R단계 (Refine ⑦)** — `src/`·`tests/` 코드 **스멜 탐지만** 수행한다. **수정·commit 금지.**

SSOT: `.cursorrules` · `src/` · `tests/` · `Report/*.REPORT.md`

**magic-square-tdd Skill이 있으면 자동 따름**

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

| 항목 | 값 | 의미 |
|------|-----|------|
| **Phase** | `refactor` | 탐지만 — 구현 변경은 `/refactor-safe` |
| **Scope** | `src/ tests/` | 검사 대상 경로 |
| **Track** | `Logic+UI` | Logic·UI 모두 점검 (본 세션 UI 없으면 Logic 위주 보고) |

---

## 전제 조건 (미충족 시 즉시 중단)

```bash
python -m pytest tests/ -v
```

| 결과 | 동작 |
|------|------|
| **전부 PASS** | 스멜 탐지 진행 |
| **하나라도 FAIL** | **중단** — 실패 Test ID·메시지 보고 후 종료. 스멜 표·후보 출력 **하지 않음** |

중단 보고 예:

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

## 전제 실패 — 중단
- pytest: N failed, M passed
- 첫 실패: test_… — …
- 조치: GREEN 복구 후 /refactor-smell 재실행
```

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `src/`·`tests/` **읽기**·정적 분석 | `src/`·`tests/` **파일 수정** |
| 스멜 표·후보 **채팅 출력** | `/refactor-safe` 자동 실행 |
| pytest **실행** (전제 확인용) | git commit·staging |
| | assert·테스트 완화 |
| | 스멜 “수정”을 위한 코드 편집 |

---

## 스멜 유형 (점검 항목)

| 유형 | 설명 | MagicSquare_xx 힌트 |
|------|------|---------------------|
| **Long Method** | 한 함수가 다중 책임·과도한 분기·길이 | `validate_lines` 본문 40줄+ |
| **Duplicated Code** | 동일·유사 로직 반복 | 행/열/대각 합 계산 복붙 |
| **Mysterious Name** | 의도 불명 변수·함수명 | `x`, `tmp`, `do_check` |
| **Magic Number** | 이름 없는 리터럴 | `34`, `16`, `4` — `MAGIC_CONSTANT` 등 미사용 |
| **ECB 위반** | Entity가 UI·이벤트 의존 | `validate_lines`에서 emit·GridUI 참조 |
| **Feature Envy** | 타 객체 데이터를 과도 사용 | 헬퍼가 grid 내부만 다루며 소유 클래스 무시 |

---

## 우선순위 (P0 / P1 / P2)

| 등급 | 기준 | 예 |
|------|------|-----|
| **P0** | 테스트·계약·가독성에 **직접** 위험 | ECB 위반, Magic Number in Control, Long Method in 진입점 |
| **P1** | 유지보수 비용·중복 | Duplicated Code, Mysterious Name |
| **P2** | 스타일·미세 개선 | docstring·주석·사소한 naming |

한 항목에 복수 유형 표기 가능 (예: `P0 · Long Method · Magic Number`).

---

## Change Budget (`/refactor-safe` 예산)

이번 세션에서 **한 번의 safe 리팩터**가 소비할 **상한**. 탐지 단계에서는 **예산만 제안**, 소비하지 않음.

| 항목 | 상한 |
|------|------|
| **파일** | ≤ 3 |
| **클래스** | ≤ 1 |
| **메서드** | ≤ 3 |

후보 제안 시 예상 소비를 표에 적는다 (예: `파일 1 · 메서드 1`).

---

## 작업 절차

1. `python -m pytest tests/ -v` 실행 → 전부 PASS 확인 (아니면 중단).
2. `src/`·`tests/` 정적 읽기 — 스멜 유형별 스캔.
3. 스멜 표 작성 (P0/P1/P2 + 유형 + 위치 + 근거 한 줄).
4. Change Budget 내 **후보 1~3개** 선정 → `/refactor-safe` 넘김 목록.
5. 사용자에게 **P0 1개만** 골라 `/refactor-safe` 실행 안내.

---

## 출력 형식 (필수)

### 블록 1 — 스멜 표

| P | 유형 | 위치 | 근거 | 예상 Budget |
|---|------|------|------|-------------|
| P0 | Magic Number | `src/validate_lines.py:…` | 리터럴 `34` 반복 | 파일 1 · 메서드 1 |
| P1 | Duplicated Code | `src/…` | 행/열 합 로직 3회 | 파일 1 · 메서드 2 |
| P2 | Mysterious Name | `tests/…` | `g` 등 | 파일 1 · 메서드 1 |

- **위치:** `경로:줄` 또는 `경로::함수명`
- **근거:** 관찰 사실 한 줄 (추측·수정안 제외)

### 블록 2 — `/refactor-safe` 후보 (1~3개)

| # | 후보 ID | P | 요약 | Budget | safe 시 기대 |
|---|---------|---|------|--------|--------------|
| 1 | RF-01 | P0 | `34` → `MAGIC_CONSTANT` 통일 | 파일 1 · 메서드 1 | Magic Number 제거, 테스트 green 유지 |
| 2 | RF-02 | P1 | 행 합 헬퍼 추출 | 파일 1 · 메서드 2 | Duplicated Code 축소 |
| 3 | RF-03 | P2 | 테스트 변수명 정리 | 파일 1 · 메서드 1 | Mysterious Name 개선 |

- 후보는 **P0 우선** 정렬.
- Budget 상한 초과 후보는 표에 넣지 않거나 «Budget 초과»로 제외.

### 블록 3 — pytest 전제

```
pytest: python -m pytest tests/ -v → PASSED (N tests)
```

---

## 완료 보고

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

## pytest 전제
- PASSED — N tests

## 스멜 요약
- P0: k건 · P1: m건 · P2: n건

## /refactor-safe 후보
1. RF-01 (P0) — …
2. RF-02 (P1) — …

## 다음
- P0 **1개만** 골라 `/refactor-safe` 실행 (예: RF-01)
```

마지막 한 줄:

```
/refactor-safe 에 넘길 후보 준비됐다 — P0 1개를 선택하세요
```

---

## 금지 (재확인)

- `src/`·`tests/` **코드 수정**
- git commit·push
- pytest FAIL 상태에서 스멜 표 출력
- 한 번에 여러 P0를 `/refactor-safe`에 동시 지시
- Change Budget 초과 리팩터를 후보로 제시
- `@pytest.mark.skip`, `xfail`, assert 완화

## 다음 단계

- **P0 1개** 선택 후 안전 리팩터: `/refactor-safe`
- 리팩터 후: `pytest` 재실행 → 필요 시 `/refactor-smell` 반복
