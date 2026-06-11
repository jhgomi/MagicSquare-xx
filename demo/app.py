"""MagicSquare_xx — PyQt6 최소 데모 (Boundary).

4×4 격자 입력 → validate_lines → status·failed_lines 표시.
Control(src/validate_lines.py)은 수정하지 않는다.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from boundary.grid_io import format_grid_for_display, parse_grid_texts  # noqa: E402
from boundary.status_display import (  # noqa: E402
    format_failed_lines_line,
    format_status_line,
    STATUS_STYLE,
)
from entity.constants import GRID_SIZE  # noqa: E402
from validate_lines import validate_lines  # noqa: E402

SAMPLE_GRIDS: dict[str, list[list[int]]] = {
    "미완성": [
        [16, 3, 0, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 0],
    ],
    "대각선 오류": [
        [5, 10, 11, 8],
        [16, 3, 2, 13],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ],
    "정답": [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ],
}


class MagicSquareDemo(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MagicSquare_xx — 10선 검증 데모")
        self.setMinimumSize(420, 380)

        self._cells: list[list[QLineEdit]] = []
        self._build_ui()
        self._load_grid(SAMPLE_GRIDS["미완성"])

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        hint = QLabel("0 = 빈칸 · 1~16 입력 · 「검증」으로 10선 판정")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint)

        grid_box = QGroupBox("4×4 격자")
        grid_layout = QGridLayout(grid_box)
        grid_layout.setSpacing(6)

        cell_font = QFont()
        cell_font.setPointSize(14)

        for row in range(GRID_SIZE):
            row_cells: list[QLineEdit] = []
            for col in range(GRID_SIZE):
                edit = QLineEdit()
                edit.setFont(cell_font)
                edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
                edit.setMaxLength(2)
                edit.setFixedSize(52, 44)
                grid_layout.addWidget(edit, row, col)
                row_cells.append(edit)
            self._cells.append(row_cells)

        layout.addWidget(grid_box, alignment=Qt.AlignmentFlag.AlignCenter)

        sample_row = QHBoxLayout()
        for name in SAMPLE_GRIDS:
            btn = QPushButton(name)
            btn.clicked.connect(lambda _checked, n=name: self._load_grid(SAMPLE_GRIDS[n]))
            sample_row.addWidget(btn)
        layout.addLayout(sample_row)

        validate_btn = QPushButton("검증")
        validate_btn.setFixedHeight(36)
        validate_btn.clicked.connect(self._on_validate)
        layout.addWidget(validate_btn)

        self._result_label = QLabel("결과: —")
        self._result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._result_label)

        self._failed_label = QLabel("")
        self._failed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._failed_label.setWordWrap(True)
        layout.addWidget(self._failed_label)

    def _load_grid(self, grid: list[list[int]]) -> None:
        display = format_grid_for_display(grid)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self._cells[r][c].setText(display[r][c])
        self._result_label.setText("결과: —")
        self._result_label.setStyleSheet("")
        self._failed_label.setText("")

    def _read_grid(self) -> list[list[int]] | None:
        text_rows = [
            [self._cells[r][c].text() for c in range(GRID_SIZE)]
            for r in range(GRID_SIZE)
        ]
        return parse_grid_texts(text_rows)

    def _on_validate(self) -> None:
        grid = self._read_grid()
        if grid is None:
            QMessageBox.warning(self, "입력 오류", "각 칸에는 빈칸 또는 1~16 정수만 입력하세요.")
            return

        result = validate_lines(grid)
        status = result["status"]
        failed = result["failed_lines"]

        self._result_label.setText(format_status_line(status))
        self._result_label.setStyleSheet(STATUS_STYLE[status])
        self._failed_label.setText(format_failed_lines_line(status, failed))


def main() -> None:
    app = QApplication(sys.argv)
    window = MagicSquareDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
