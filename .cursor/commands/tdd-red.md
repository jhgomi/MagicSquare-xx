# tdd-red

`validate_lines` TDD **RED** 단계만 수행한다. `.cursorrules`와 동일한 계약을 따른다.

## Phase 선언

- 응답 **첫 줄**에 반드시: `Phase: RED`
- RED가 끝나면 GREEN·REFACTOR로 넘어가지 않는다. 구현(`src/`)은 하지 않는다.

## 수정 범위

| 허용 | 금지 |
|------|------|
| `tests/` (주로 `tests/test_validate_lines.py`) | `src/` 전체 (`validate_lines.py` 포함) |
| 테스트용 fixture·격자 상수 | `@pytest.mark.skip`, `xfail`, assert 완화·삭제 |
| | 테스트를 통과시키려는 production 코드 선행 작성 |

## AAA 절차

각 테스트는 **한 행동·한 검증**만. 순서:

1. **Arrange** — 4×4 격자(중첩 `list[list[int]]`)와 기대값 준비. `0`=빈칸, 1~16, 마법상수 34, 10선 ID `R1`~`R4`·`C1`~`C4`·`D1`·`D2`.
2. **Act** — `result = validate_lines(grid)` 호출.
3. **Assert** — 반환 dict 계약 검증:
   - `result["status"]` ∈ `"pass"` | `"fail"` | `"incomplete"`
   - `result["failed_lines"]`는 `list[str]`
   - pass·incomplete → `failed_lines == []`
   - fail → 깨진 축 ID 포함 (예 `"D1"`, `"D2"`)

## RED 우선 케이스 (Boundary)

| # | 테스트 의도 | 기대 status |
|---|-------------|---------------|
| 1 | `0` 포함 격자 | `incomplete` |
| 2 | 행·열 34, 대각선만 틀림 | `fail` + `D1`/`D2` |
| 3 | 행·열만 34인 가짜 완료 | `fail` |
| 4 | 정답 4×4 마방진 | `pass` |

한 사이클에 **테스트 하나**만 RED까지 완료해도 된다.

## pytest 예시

```python
def test_diagonal_only_wrong_returns_fail():
    # Arrange — 행·열 합 34, D1(주대각)만 34 아님
    grid = [
        [16,  3,  2, 13],
        [ 5, 10, 11,  8],
        [ 9,  6,  7, 12],
        [ 4, 15, 14,  1],
    ]
    # Act
    result = validate_lines(grid)
    # Assert
    assert result["status"] == "fail"
    assert "D1" in result["failed_lines"]
    assert result["failed_lines"] == sorted(result["failed_lines"])  # 선택: 순서 고정 시
```

실행:

```bash
python -m pytest tests/test_validate_lines.py -v
```

**성공 기준:** 새·수정 테스트가 **실패**해야 RED 완료 (`FAILED` 또는 `AssertionError`). 전부 green이면 assert가 빠졌거나 `src/`가 이미 구현된 상태 — RED 아님.

## RED 완료 보고 형식

작업 후 아래 형식으로 짧게 보고:

```
Phase: RED

## 변경
- tests/test_validate_lines.py: <추가/수정한 테스트명>

## Arrange
- <격자 요약 또는 케이스 한 줄>

## Assert
- status: <기대값>
- failed_lines: <기대값>

## pytest
- 명령: python -m pytest tests/test_validate_lines.py::<test_name> -v
- 결과: FAILED — <실패 메시지 한 줄>

## 다음
- GREEN: src/validate_lines.py 최소 구현 (별도 명령)
```

## 금지 (재확인)

- `src/` 수정·생성
- assert 조건 완화, `==` → `in` 축소, 기대값 삭제
- `@pytest.mark.skip`, `pytest.skip`, `xfail`
- RED 단계에서 `validate_lines` 본문 구현
- git commit (사용자 요청 시만)
