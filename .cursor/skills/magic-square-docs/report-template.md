# Report Template — `Report/{NN}.REPORT.md`

SSOT 형식: `Report/05.REPORT.md` (TDD·ARRR 1사이클 Export). `NN` = Step B에서 계산.

---

```markdown
# MagicSquare_xx STEP {N} — {제목 한 줄}

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_xx / MagicSquare_1004 |
| **경로** | `c:\김정화\DEV\MagicSquare_xx` |
| **작성일** | {YYYY-MM-DD} |
| **단계** | STEP {N} — {Phase 요약} |
| **Phase** | {red \| green \| refactor \| repeat} |
| **Test ID** | {T-…, RF-… 목록} |
| **Command** | {/red-test-plan, …} |
| **참고** | [Report/{이전}.REPORT.md]({이전}.REPORT.md) |
| **Transcript** | [Prompting/{NN}.Export-Transcript.md](../Prompting/{NN}.Export-Transcript.md) |

---

## 1. 개요

{ARRR 1사이클 또는 repeat 요약 2~4문장. 세션 주제·달성·미완 한 줄.}

| 항목 | 내용 |
|------|------|
| **ARRR** | Ask / Respond / Refine / Repeat |
| **Track** | Logic \| UI (+ Layer: entity \| boundary) |
| **판정** | ✅ 완료 \| ⚠️ 부분 \| ❌ 중단 |

---

## 2. 실행 증거 (Step A 실측)

### 2.1 pytest

```bash
python -m pytest tests/ -v
```

| 항목 | 결과 |
|------|------|
| **명령** | `python -m pytest tests/ -v` |
| **결과** | {PASSED N \| FAILED …} — **실행 출력만** |
| **Test ID** | {관련 ID} |

### 2.2 git status

| 항목 | 내용 |
|------|------|
| **브랜치** | {branch} |
| **변경** | {modified / untracked 요약} |
| **commit** | 없음 (Export만) |

---

## 3. Phase별 STEP

> 완료된 Phase만 채운다. 미실시 STEP은 «해당 없음».

### 3.1 STEP: RED

| 항목 | 내용 |
|------|------|
| **Test ID** | {T-INC-01, …} |
| **Command** | `/red-test-plan` → `/red-skeleton` → `/tdd-red` |
| **C2C** | Rule1~3 요약 1줄 |
| **변경** | `tests/…` |
| **pytest** | FAILED — {메시지 한 줄} |

### 3.2 STEP: GREEN

| 항목 | 내용 |
|------|------|
| **Test ID** | {…} |
| **Command** | `/green-minimal` \| `/golden-master` |
| **변경** | `src/validate_lines.py`, … |
| **pytest** | PASSED — {N} tests |
| **golden** | {matched yes/no \| 해당 없음} |

### 3.3 STEP: REFACTOR

| 항목 | 내용 |
|------|------|
| **RF-xx** | {RF-01, …} |
| **Command** | `/refactor-smell` → `/refactor-safe` |
| **Budget** | 파일 {n} · 클래스 {n} · 메서드 {n} |
| **pytest** | PASSED |
| **golden** | matched: {yes \| rolled back \| n/a} |

### 3.4 STEP: repeat

| 항목 | 내용 |
|------|------|
| **이전 Report** | [Report/{이전}.REPORT.md]({이전}.REPORT.md) |
| **반복 사유** | {Phase: repeat 이유} |
| **delta** | {이번 NN에서 추가된 것만} |

---

## 4. 변경 파일

| 경로 | Phase | 요약 |
|------|-------|------|
| `tests/test_validate_lines.py` | RED | … |
| `src/validate_lines.py` | GREEN | … |

---

## 5. 산출물·폴더

```
c:\김정화\DEV\MagicSquare_xx\
├── Report/
│   └── {NN}.REPORT.md          # 본 보고서
├── Prompting/
│   └── {NN}.Export-Transcript.md
└── …
```

---

## 6. 판정·다음

| 항목 | 판정 |
|------|------|
| ARRR 1사이클 | {✅ \| ⚠️ \| ❌} |
| pytest | {실측 요약} |
| 다음 | {다음 Command·Test ID} |
```

---

## 작성 규칙

- 표·헤더 순서는 위 템플릿 **유지**.
- pytest·git은 Step A **실행 결과만** — 추정·이전 채팅 인용 금지 (채팅에 pytest 없으면 «미실행»).
- `UPDATE_GOLDEN` 사용 시 GREEN/REFACTOR STEP에 **명시** (임의 실행 금지).
- 한국어 본문.
