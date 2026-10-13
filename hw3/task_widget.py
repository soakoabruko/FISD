#!/usr/bin/env python3
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from task import Task


class TaskWidget(QWidget):
    def __init__(self, task: Task) -> None:
        super().__init__()

        root = QHBoxLayout(self)

        completed_emoji_label = QLabel("✅" if task.is_completed else "")

        body_layout = QVBoxLayout()
        title_label = QLabel(task.title)
        desc_label = QLabel(task.desc)
        priority_label = QLabel(task.priority)
        body_layout.addWidget(title_label)
        body_layout.addWidget(desc_label)
        body_layout.addWidget(priority_label)

        pinned_emoji_label = QLabel("📌" if task.is_pinned else "")

        root.addWidget(completed_emoji_label)
        root.addLayout(body_layout)
        root.addWidget(pinned_emoji_label)