"""UI Track — 검증 status·failed_lines 표시 문자열."""

STATUS_STYLE = {
    "pass": "color: #1b7f3a; font-weight: bold;",
    "fail": "color: #c0392b; font-weight: bold;",
    "incomplete": "color: #d68910; font-weight: bold;",
}

STATUS_LABEL = {
    "pass": "pass — 10선 모두 34",
    "fail": "fail — 깨진 축 있음",
    "incomplete": "incomplete — 빈칸(0) 존재",
}


def format_status_line(status: str) -> str:
    return f"결과: {STATUS_LABEL[status]}"


def format_failed_lines_line(status: str, failed_lines: list[str]) -> str:
    if failed_lines:
        return f"failed_lines: {', '.join(failed_lines)}"
    if status == "incomplete":
        return "failed_lines: [] (빈칸 채운 뒤 재검증)"
    return "failed_lines: []"
