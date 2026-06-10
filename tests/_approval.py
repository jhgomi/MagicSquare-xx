from pathlib import Path
import os

GOLDEN_DIR = Path(__file__).parent / "golden"


def format_golden(actual: dict, int6: list[int]) -> str:
    """int[6] 1-index + ERR 한 줄 — 포맷 고정."""
    failed = ",".join(sorted(actual["failed_lines"])) if actual["failed_lines"] else "none"
    int6_line = "INT6 " + " ".join(str(x) for x in int6)
    err_line = f"ERR status={actual['status']} failed={failed}"
    return f"{int6_line}\n{err_line}\n"


def assert_matches_golden(test_id: str, actual_text: str) -> None:
    """UPDATE_GOLDEN=1 이면 기준 생성; 아니면 diff 비교."""
    golden_path = GOLDEN_DIR / f"{test_id.lower()}.approved.txt"
    golden_path.parent.mkdir(parents=True, exist_ok=True)

    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.write_text(actual_text, encoding="utf-8")
        return

    if not golden_path.exists():
        raise AssertionError(f"golden missing: {golden_path} — run UPDATE_GOLDEN=1 first")

    expected = golden_path.read_text(encoding="utf-8")
    if actual_text != expected:
        raise AssertionError(
            f"golden mismatch: {golden_path}\n--- expected ---\n{expected}--- actual ---\n{actual_text}"
        )
