#!/usr/bin/env python3
from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QRadioButton, QCheckBox, QPushButton
)
from task import Task


class TaskDialog(QDialog):
    def __init__(self, parent: QWidget | None=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Новая задача")
        self.resize(400, 600)

        root = QVBoxLayout(self)

        title_layout = QHBoxLayout()
        title_label = QLabel("Название:")
        self._title_line_edit = QLineEdit()
        title_layout.addWidget(title_label)
        title_layout.addWidget(self._title_line_edit)

        desc_label = QLabel("Описание:")
        self._desc_text_edit = QTextEdit()

        priority_label = QLabel("Приоритет:")
        priority_layout = QHBoxLayout()
        self._radio_low = QRadioButton("Низкий")
        self._radio_medium = QRadioButton("Средний")
        self._radio_high = QRadioButton("Высокий")
        self._radio_medium.setChecked(True)
        priority_layout.addWidget(self._radio_low)
        priority_layout.addWidget(self._radio_medium)
        priority_layout.addWidget(self._radio_high)

        extra_label = QLabel("Дополнительные настройки:")
        self._checkbox_complete = QCheckBox("Отметить выполненной")
        self._checkbox_pin = QCheckBox("Закрепить")

        button_layout = QHBoxLayout()
        button_clear = QPushButton("Очистить")
        button_create = QPushButton("Создать")
        button_clear.clicked.connect(self._on_clear)
        button_create.clicked.connect(self.accept)
        button_layout.addWidget(button_clear)
        button_layout.addWidget(button_create)

        root.addLayout(title_layout)
        root.addWidget(desc_label)
        root.addWidget(self._desc_text_edit)
        root.addWidget(priority_label)
        root.addLayout(priority_layout)
        root.addWidget(extra_label)
        root.addWidget(self._checkbox_complete)
        root.addWidget(self._checkbox_pin)
        root.addLayout(button_layout)

    def _on_clear(self) -> None:
        self._title_line_edit.setText("")
        self._desc_text_edit.setText("")
        self._radio_medium.setChecked(True)
        self._checkbox_complete.setChecked(False)
        self._checkbox_pin.setChecked(False)

    def get_task(self) -> Task:
        title = self._title_line_edit.text()
        desc = self._desc_text_edit.toPlainText()
        priority = 'Средний'

        if self._radio_low.isChecked():
            priority = 'Низкий'
        elif self._radio_high.isChecked():
            priority = 'Высокий'

        is_completed = self._checkbox_complete.isChecked()
        is_pinned = self._checkbox_pin.isChecked()

        return Task(title, desc, priority, is_completed, is_pinned)