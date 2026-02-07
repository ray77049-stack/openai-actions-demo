"""Offline desktop monitor launcher UI (MVP stub)."""

from __future__ import annotations

import sys
from datetime import datetime

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Offline Monitor (MVP)")
        self.resize(640, 420)

        self.status_label = QLabel("狀態：待機")
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)

        self.start_btn = QPushButton("開始監控")
        self.stop_btn = QPushButton("停止監控")
        self.stop_btn.setEnabled(False)

        self.start_btn.clicked.connect(self.start_monitoring)
        self.stop_btn.clicked.connect(self.stop_monitoring)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.log_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.heartbeat_timer = QTimer(self)
        self.heartbeat_timer.setInterval(5000)
        self.heartbeat_timer.timeout.connect(self.write_heartbeat)

    def start_monitoring(self) -> None:
        self.status_label.setText("狀態：監控中")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log("Monitoring started.")
        self.heartbeat_timer.start()

    def stop_monitoring(self) -> None:
        self.status_label.setText("狀態：已停止")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.log("Monitoring stopped.")
        self.heartbeat_timer.stop()

    def write_heartbeat(self) -> None:
        self.log("Heartbeat OK (stub).")

    def log(self, message: str) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_view.append(f"[{now}] {message}")


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
