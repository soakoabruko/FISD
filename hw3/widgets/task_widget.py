#!/usr/bin/env python3
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from task import Task


class TaskWidget(QWidget):
    deleted = pyqtSignal(int)

    def _on_delete_task(self) -> None:
        message = QMessageBox()
        message.setWindowTitle("Предупреждение")
        message.setIcon(QMessageBox.Icon.Warning)
        message.setText("Задача будет удалена. Продолжить?")
        message.setStandardButtons(
            QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok
        )

        if message.exec() == QMessageBox.StandardButton.Ok:
            self.deleted.emit(self._task.task_id)

    def __init__(self, task: Task) -> None:
        super().__init__()
        self._task = task

        root = QHBoxLayout(self)

        if self._task.is_pinned or self._task.is_completed:
            extra_layout = QVBoxLayout()

            if self._task.is_pinned:
                pinned_emoji_label = QLabel("📌")
                extra_layout.addWidget(pinned_emoji_label)

            if self._task.is_completed:
                completed_emoji_label = QLabel("✅")
                extra_layout.addWidget(completed_emoji_label)
            
            root.addLayout(extra_layout)

        body_layout = QVBoxLayout()

        title_label = QLabel(self._task.title)
        body_layout.addWidget(title_label)

        if self._task.desc.strip():
            desc_label = QLabel(self._task.desc)
            desc_label.setWordWrap(True)
            body_layout.addWidget(desc_label)

        if self._task.priority:
            priority_label = QLabel(self._task.priority)
            body_layout.addWidget(priority_label)

        root.addLayout(body_layout)

        button_layout = QVBoxLayout()

        delete_button = QPushButton("🗑️")
        delete_button.clicked.connect(self._on_delete_task)
        button_layout.addWidget(delete_button)

        root.addLayout(button_layout)