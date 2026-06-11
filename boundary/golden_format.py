"""UI Track — Golden Master INT6·ERR 직렬화."""

def format_golden(actual: dict, int6: list[int]) -> str:
    """int[6] 1-index + ERR 한 줄 — 포맷 고정."""
    failed = ",".join(sorted(actual["failed_lines"])) if actual["failed_lines"] else "none"
    int6_line = "INT6 " + " ".join(str(x) for x in int6)
    err_line = f"ERR status={actual['status']} failed={failed}"
    return f"{int6_line}\n{err_line}\n"
