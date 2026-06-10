# Transcript Template — `Prompting/{NN}.Export-Transcript.md`

SSOT 형식: `Prompting/05.Export-Transcript.md`. 파일명 규칙: `{NN}.Export-Transcript.md` (기존 `NN.REPORT.md`와 구분).

---

```markdown
# MagicSquare_xx STEP {N} — {제목} (대화 기록)

_Exported on {M/D/YYYY} from Cursor — MagicSquare_xx workspace_
_Source: {uuid}_

**Report:** [Report/{NN}.REPORT.md](../Report/{NN}.REPORT.md)

---

**User**

{사용자 메시지 요약 또는 원문 — Export 대상 턴부터}

---

**Cursor**

{Phase 선언 첫 줄}
{응답 요약 — 표·경로·판정}

---

**User**

{다음 사용자 메시지}

---

**Cursor**

{다음 응답}

---

… (User / Cursor 교차 반복) …

---

**User**

/export-session

---

**Cursor**

`Report/{NN}.REPORT.md` · `Prompting/{NN}.Export-Transcript.md` 생성.

**보고서:** [Report/{NN}.REPORT.md](../Report/{NN}.REPORT.md)

---

## 생성 파일

| 폴더 | 파일 |
|------|------|
| `Report/` | `{NN}.REPORT.md` — {제목} |
| `Prompting/` | `{NN}.Export-Transcript.md` — 본 transcript |
```

---

## 헤더 필드

| 필드 | 규칙 |
|------|------|
| **_Exported on** | Export 당일. 형식: `6/10/2026` (M/D/YYYY, 선행 0 없음) |
| **_Source** | agent transcript `uuid` (`.jsonl` 파일명, `.jsonl` 제외). 없으면 `_Source: n/a` |
| **제목** | Report `STEP {N}` 제목과 **동일** |

## User / Cursor 블록

- 구분선 `---` 로 턴 분리.
- **User** / **Cursor** 볼드 라벨 후 빈 줄, 본문.
- Cursor 블록: Phase 선언·파일 경로·표 **요약** (전문 붙여넣기는 핵심 턴만).
- Command 호출은 백틱: `/red-test-plan`, `/export-session`.
- `@파일` 참조 유지.

## Source uuid 찾기

1. Cursor agent transcripts: `agent-transcripts/{uuid}.jsonl`
2. 현재 세션 ID가 있으면 해당 uuid
3. 없으면 `_Source: n/a` — **임의 uuid 생성 금지**

## 작성 규칙

- Export **대상 세션** 턴만 포함 (이전 Report에 있는 내용 전량 복사 금지).
- pytest 결과는 **채팅 또는 Step A 실행**에 있는 것만.
- 마지막 턴: `/export-session` 요청·생성 확인.
- 한국어.
