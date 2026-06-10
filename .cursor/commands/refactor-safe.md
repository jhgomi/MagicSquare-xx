# refactor-safe

`/refactor-smell` 표에서 **선택한 스멜 1개만** Safe Refactor 실행한다. 동작·계약은 유지한다.

SSOT: 직전 `/refactor-smell` 후보(RF-xx) · `.cursorrules` · `src/` · `tests/`

**magic-square-tdd Skill이 있으면 자동 따름**

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: refactor | Layer: entity | Track: Logic
```

| 항목 | 값 | 기본 |
|------|-----|------|
| **Phase** | `refactor` | 구조 개선만 — 기능 변경은 GREEN |
| **Layer** | `entity` \| `boundary` | smell 위치 따름; 기본 `entity` |
| **Track** | `Logic` \| `UI` | 기본 `Logic` |

---

## 선행 조건

| 항목 | 요구 |
|------|------|
| **선택** | `/refactor-smell` 후보 **1개** (RF-xx · P0 권장) |
| **pytest** | 실행 전·후 `python -m pytest tests/ -v` **전부 PASS** |
| **Budget** | `refactor-smell` 예상 Budget 이내 (파일≤3 · 클래스≤1 · 메서드≤3) |

후보·스멜 표가 채팅에 없으면 직전 `/refactor-smell` 출력에서 RF-xx를 가져온다. **복수 스멜 동시 수정 금지.**

---

## Safe Refactor 원칙 (불변)

| 항목 | 규칙 |
|------|------|
| **입출력** | `validate_lines(grid) -> dict` 시그니처·키·값 의미 **동일** |
| **예외** | 발생 조건·타입·메시지 **변경 금지** |
| **int[6] 1-index** | Golden·직렬화 6정수·1-based 좌표 **변경 금지** |
| **ERR 문자열** | `ERR status=… failed=…` 포맷 **변경 금지** |
| **E001~E005** | ECB emit·GridUI 이벤트 **금지** |
| **기능** | 새 요구·버그 수정 **금지** — 별도 GREEN 사이클 |
| **테스트** | assert 완화·skip·xfail **금지** |

허용: 이름 개선·추출 함수·중복 제거·상수 참조·구조 분리 (**관찰 가능 동작 동일**).

---

## Change Budget (준수 필수)

| 항목 | 상한 | 초과 시 |
|------|------|---------|
| **파일** | ≤ 3 | 작업 **중단**·범위 축소 후 재시도 |
| **클래스** | ≤ 1 | 동일 |
| **메서드** | ≤ 3 | 동일 (신규 private 헬퍼 포함) |

Budget 소비는 완료 보고에 **실제 수치**로 기록한다.

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `src/` — 선택 스멜 1건 구조 개선 | 스멜 표에 없는 **추가** 리팩터 |
| `tests/` — import·이름 정리 (동작 동일) | assert·기대값 변경 |
| `entity/constants.py` — 상수 **참조** 정리 | 기능 추가·버그 수정 |
| | `tests/golden/*.approved.txt` **수동 편집** |
| | git commit (사용자 요청 시만) |

---

## 작업 절차

1. 대상 **RF-xx 1개** 확인 (유형·위치·Budget).
2. Safe 원칙·Budget 재확인.
3. **최소 diff**로 리팩터 (`src/` 중심, 필요 시 `tests/` import만).
4. `python -m pytest tests/ -v` — 전부 PASS.
5. Golden 검증 (`UPDATE_GOLDEN` **설정 없음**):

```bash
python -m pytest tests/ -v -k golden
```

또는 approval 테스트 전체:

```bash
python -m pytest tests/ -v
```

6. golden 결과에 따라 분기 (아래).
7. 완료 보고.

---

## Golden diff 분기

| 상황 | 조치 |
|------|------|
| **matched** | 완료 보고 → 종료 |
| **diff · 비의도** | **롤백** — 리팩터 변경 되돌림 → pytest 재실행 PASS 확인 → 보고 |
| **diff · 의도적** | Golden 직렬화 경로가 구조 변경에 **필수적으로** 연동된 경우만 |

의도적 diff 처리 (순서 고정):

1. **ISS 문서화** — 채팅·`Report/`에 한 줄: RF-xx, diff 요약, 왜 의도적인지.
2. `UPDATE_GOLDEN=1 python -m pytest tests/ -v -k golden` — 기준 **재생성**.
3. `UPDATE_GOLDEN` 없이 재실행 → **matched** 확인.

```
ISS: RF-01 — format_golden 호출부만 이동, INT6/ERR 출력 동일 유지
```

**금지:** diff를 golden 수동 편집으로 맞추기.

---

## 스멜 유형별 Safe 가이드

| 유형 | Safe 예 | Unsafe (금지) |
|------|---------|----------------|
| **Magic Number** | `MAGIC_CONSTANT` import·치환 | 상수 **값** 변경 |
| **Duplicated Code** | `_sum_row` private 추출 | 합 계산 **로직** 변경 |
| **Long Method** | 조기 return·헬퍼 분리 | 분기 순서 변경으로 status 바뀜 |
| **Mysterious Name** | `grid` → `square_grid` | public API 이름 변경 |
| **Feature Envy** | grid 인자 명시 헬퍼 | 데이터 소유 경계 변경 |
| **ECB 위반** | UI import **제거** | emit 추가 |

---

## 완료 보고 형식

```
Phase: refactor | Layer: entity | Track: Logic

## 대상
- RF-01 (P0) — Magic Number · src/validate_lines.py

## 변경 요약
- src/validate_lines.py: 리터럴 34 → MAGIC_CONSTANT (동작 동일)
- Budget: 파일 1 · 클래스 0 · 메서드 1

## pytest
- python -m pytest tests/ -v → PASSED (N tests)

## golden
- matched: yes | no (rolled back | ISS + UPDATE_GOLDEN)
- 경로: tests/golden/t-inc-01.approved.txt (해당 시)

## diff (matched=no였을 때)
- …
```

마지막 한 줄 (pytest PASS · golden matched):

```
Safe Refactor 완료 — /refactor-smell 재실행 가능
```

롤백 시:

```
Safe Refactor 롤백 — 비의도 golden diff, 변경 되돌림 완료
```

---

## 금지 (재확인)

- 스멜 **2개 이상** 동시 수정
- Change Budget 초과
- 입출력·예외·int[6]·ERR 포맷 변경
- E001~E005 emit
- 기능 추가·버그 수정 (GREEN으로 분리)
- `@pytest.mark.skip`, `xfail`, assert 완화
- golden 수동 편집
- pytest FAIL 상태에서 완료 보고

## 다음 단계

- 추가 스멜: `/refactor-smell` → P0 1개 선택 → `/refactor-safe` 반복
- 기능 변경 필요: RED → GREEN 별도 사이클
