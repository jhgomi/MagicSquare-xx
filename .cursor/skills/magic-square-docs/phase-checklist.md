# Phase Export Checklist

`/export-session` · Report Export · Transcript 작성 전 **순서대로** 확인.

## 진입 조건

- [ ] 사용자가 Export·`/export-session`·세션 보고서를 **명시** 요청
- [ ] `magic-square-docs` Skill 로드됨
- [ ] ARRR 1사이클 완료 또는 `Phase: repeat` 보고 대상

## Step A — 입력 수집

- [ ] `git status` 실행·결과 기록 (임의 commit **금지**)
- [ ] `python -m pytest tests/ -v` 실행·결과 기록 (**채팅에 없는 결과 기재 금지**)
- [ ] 채팅에서 **Phase** 추출 (`red` | `green` | `refactor` | `repeat`)
- [ ] **Test ID** 목록 추출 (예: `T-INC-01`, `RF-01`)
- [ ] 사용 **Command** 목록 추출 (예: `/red-test-plan`, `/green-minimal`)
- [ ] Transcript **Source uuid** 확인 (agent transcript 있으면; 없으면 `n/a` 명시)

## Step B — 번호 (NN)

- [ ] `Report/` 내 `NN.REPORT.md` 최대 NN 확인
- [ ] `Prompting/` 내 `NN.*.md` 최대 NN 확인
- [ ] `NN = max(Report, Prompting) + 1` 계산
- [ ] 파일명 확정: `Report/{NN}.REPORT.md`, `Prompting/{NN}.Export-Transcript.md`

## Step C — Report

- [ ] [report-template.md](report-template.md) 적용
- [ ] Phase별 **STEP** 섹션 채움 (RED / GREEN / REFACTOR / repeat)
- [ ] pytest·git·변경 파일은 **Step A 실측만** 사용
- [ ] Transcript 상대 링크: `../Prompting/{NN}.Export-Transcript.md`

## Step D — Transcript

- [ ] [transcript-template.md](transcript-template.md) 적용
- [ ] `_Exported on {날짜} from Cursor — MagicSquare_xx workspace_`
- [ ] `_Source: {uuid}` (또는 `n/a`)
- [ ] **User** / **Cursor** 교차 기록
- [ ] Report 링크: `../Report/{NN}.REPORT.md`

## Step E — README

- [ ] `README.md` 존재 확인 — 없으면 문서 표 섹션 생성
- [ ] 문서 표에 Report·Prompting 행 **1줄 추가** (NN, 제목, Phase, 날짜)
- [ ] 기존 행 수정·삭제 없이 **추가만**

## Step F — 완료 보고

- [ ] `Report/{NN}.REPORT.md` 경로 보고
- [ ] `Prompting/{NN}.Export-Transcript.md` 경로 보고
- [ ] pytest 요약 1줄 (실측)
- [ ] git commit **하지 않음** (사용자 요청 시만)

## 금지 (재확인)

| 금지 | 이유 |
|------|------|
| git commit 임의 | 사용자 요청 전용 |
| `UPDATE_GOLDEN=1` 임의 | golden 의도적 갱신만 |
| 채팅·실행 없는 pytest 결과 | 허위 보고 |
| golden 수동 편집 반영 | SSOT 위반 |
| 기존 Report/Prompting 덮어쓰기 | NN는 항상 신규 |

## Phase → Report STEP 매핑

| Phase | STEP 섹션 | 필수 기록 |
|-------|-------------|-----------|
| `red` | RED | Test ID, Command, FAILED pytest |
| `green` | GREEN | Test ID, src 변경, PASSED pytest |
| `refactor` | REFACTOR | RF-xx, Budget, golden matched |
| `repeat` | repeat | 이전 NN 참조, 반복 사유, delta |

복수 Phase 한 세션: 해당 STEP **모두** 채움 (완료된 것만).
