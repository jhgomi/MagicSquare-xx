---
name: magic-square-docs
description: >-
  MagicSquare_xx Report·Transcript Export (ARRR 1사이클·세션 보고서).
  Use for Report Export, Transcript, /export-session, Phase repeat;
  when completing an ARRR cycle report or session N documentation.
disable-model-invocation: true
---

# magic-square-docs

Report·Transcript Export Skill. SSOT: `Report/05.REPORT.md` · `Prompting/05.Export-Transcript.md` · 기존 `Report/01`~`04` · `Prompting/01`~`04`.

**Export 요청 시 magic-square-docs Skill 로드 후 [phase-checklist.md](phase-checklist.md) 수행.**

`/export` · `/export-session` Command 실행 시 본 Skill을 따른다.

---

## 로드 조건

- 사용자가 Export·Transcript·세션 보고서·`/export-session` **명시**
- `Phase: repeat` 보고
- ARRR 1사이클 완료 보고 요청

자동 Export 추론 금지.

---

## 워크플로 (Step A → F)

### Step A — 입력 수집

**반드시 실행·채팅에서 추출.** 없으면 «미실행»·«n/a».

| 입력 | 수집 방법 |
|------|-----------|
| **git status** | `git status` 실행 |
| **pytest** | `python -m pytest tests/ -v` 실행 |
| **Phase** | 채팅 첫 줄·Command (`red` \| `green` \| `refactor` \| `repeat`) |
| **Test ID** | C2C·완료 보고 (`T-…`, `RF-…`, `D-LOC-…`) |
| **Command** | 사용한 `/red-test-plan` 등 목록 |
| **Source uuid** | agent transcript uuid 또는 `n/a` |

### Step B — NN 결정

```
NN = max(Report 폴더 NN, Prompting 폴더 NN) + 1
```

| 폴더 | 패턴 | 예 |
|------|------|-----|
| `Report/` | `{NN}.REPORT.md` | `05.REPORT.md` |
| `Prompting/` | `{NN}.Export-Transcript.md` | `05.Export-Transcript.md` |

- 두 폴더 **같은 NN** 사용.
- 기존 파일 **덮어쓰기 금지**.

### Step C — Report

1. [report-template.md](report-template.md) 복사·채움.
2. Phase별 **STEP** 섹션:
   - `red` → **STEP: RED**
   - `green` → **STEP: GREEN**
   - `refactor` → **STEP: REFACTOR**
   - `repeat` → **STEP: repeat**
3. §2 실행 증거 = Step A **실측만**.
4. 저장: `Report/{NN}.REPORT.md`

### Step D — Transcript

1. [transcript-template.md](transcript-template.md) 적용.
2. 헤더:
   - `_Exported on {M/D/YYYY} from Cursor — MagicSquare_xx workspace_`
   - `_Source: {uuid}`
3. **User** / **Cursor** 교차 — Export 대상 세션 턴.
4. 저장: `Prompting/{NN}.Export-Transcript.md`

### Step E — README 문서 표 갱신

`README.md`에 **문서 표** 섹션 유지·추가 (없으면 생성):

```markdown
## 문서

| NN | Report | Transcript | Phase | 날짜 |
|----|--------|------------|-------|------|
| 05 | [05.REPORT.md](Report/05.REPORT.md) | [05.Export-Transcript.md](Prompting/05.Export-Transcript.md) | green | 2026-06-10 |
```

- **새 행 1줄 추가만** — 기존 행 삭제·수정 최소화.
- 링크·NN·제목·Phase·작성일 일치.

### Step F — 완료 보고

채팅에 **경로 2개** + pytest 1줄:

```
## Export 완료
- Report: Report/{NN}.REPORT.md
- Transcript: Prompting/{NN}.Export-Transcript.md
- pytest: {실측 한 줄}
```

---

## Phase → Report STEP 빠른 참조

| Phase | STEP | 필수 필드 |
|-------|------|-----------|
| red | RED | Test ID, Command 체인, tests 변경, FAILED |
| green | GREEN | src 변경, PASSED, golden(optional) |
| refactor | REFACTOR | RF-xx, Budget, PASSED, golden matched |
| repeat | repeat | 이전 NN, delta, 사유 |

복수 Phase 완료 시 해당 STEP **모두** §3에 포함.

---

## Command 연동

| Command | 동작 |
|---------|------|
| `/export` | legacy — 본 Skill Step A~F (Prompting 파일명은 `{NN}.Export-Transcript.md` 우선) |
| `/export-session` | Export 요청 시 **magic-square-docs Skill 로드 후 checklist 수행** |

### `/export-session` 본문 (Command 파일용)

```markdown
# export-session

Report·Transcript Export. **magic-square-docs Skill 로드 후 [phase-checklist.md](../skills/magic-square-docs/phase-checklist.md) 수행.**

SSOT: Report/05.REPORT.md · Prompting/05.Export-Transcript.md
```

---

## 금지

| 금지 | 이유 |
|------|------|
| **git commit 임의** | 사용자 요청 시만 |
| **UPDATE_GOLDEN=1 임의** | 의도적 golden 갱신·ISS 문서화 후만 |
| **채팅에 없는 pytest 결과** | 허위 증거 |
| **임의 Source uuid** | 없으면 `n/a` |
| **기존 NN 덮어쓰기** | 항상 max+1 |
| **golden 수동 편집을 보고에 반영** | SSOT 위반 |

pytest 미실행 시 Report §2.1에 «미실행» — 추정 PASS/FAIL 기재 금지.

---

## 템플릿·체크리스트

| 파일 | 용도 |
|------|------|
| [report-template.md](report-template.md) | `Report/{NN}.REPORT.md` |
| [transcript-template.md](transcript-template.md) | `Prompting/{NN}.Export-Transcript.md` |
| [phase-checklist.md](phase-checklist.md) | Export 전후 체크 |

---

## 완료 보고 예

```
## Export 완료

| 항목 | 경로 |
|------|------|
| Report | Report/05.REPORT.md |
| Transcript | Prompting/05.Export-Transcript.md |

- Phase: green | Test ID: T-INC-01
- pytest: PASSED — 4 tests (실행함)
- README: 문서 표 NN=05 행 추가
```

---

## 관련 Skill

- TDD 워크플로: `magic-square-tdd` — Phase·Command·완료 보고 형식
- Export는 TDD **이후** 증거 고정용; RED/GREEN 본문은 TDD Skill SSOT
