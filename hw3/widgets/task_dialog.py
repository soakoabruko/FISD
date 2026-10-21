#!/usr/bin/env python3
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from task import Task
from widgets.constants import PRIORITIES


class TaskDialog(QDialog):
    def _on_clear_form(self) -> None:
        message = QMessageBox()
        message.setWindowTitle("Предупреждение")
        message.setIcon(QMessageBox.Icon.Warning)
        message.setText("Заполненные поля будут очищены. Продолжить?")
        message.setStandardButtons(
            QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok
        )

        if message.exec() == QMessageBox.StandardButton.Ok:
            self._title_line_edit.setText("")
            self._desc_text_edit.setText("")

            if PRIORITIES:
                self._radio_priorities[0].setChecked(True)
            
            self._checkbox_complete.setChecked(False)
            self._checkbox_pin.setChecked(False)

    def _on_create_task(self) -> None:
        if self._title_line_edit.text().strip():
            self.accept()
            return

        message = QMessageBox()
        message.setWindowTitle("Ошибка")
        message.setIcon(QMessageBox.Icon.Critical)
        message.setText("Название задачи не должно быть пустым или состоять из пробелов")
        message.setStandardButtons(QMessageBox.StandardButton.Ok)

        message.exec()

    def __init__(self, parent: QWidget | None=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Новая задача")
        self.resize(400, 600)

        root = QVBoxLayout(self)

        title_layout = QHBoxLayout()
        
        title_label = QLabel("Название:")
        title_layout.addWidget(title_label)

        self._title_line_edit = QLineEdit()
        title_layout.addWidget(self._title_line_edit)

        root.addLayout(title_layout)

        title_counter = QLabel("Кол-во символов: 0")
        self._title_line_edit.textChanged.connect(
            lambda: title_counter.setText(
                f"Кол-во символов: {len(self._title_line_edit.text())}"
            )
        )
        root.addWidget(title_counter)

        desc_label = QLabel("Описание:")
        root.addWidget(desc_label)

        self._desc_text_edit = QTextEdit()
        root.addWidget(self._desc_text_edit)

        desc_counter = QLabel("Кол-во символов: 0")
        self._desc_text_edit.textChanged.connect(
            lambda: desc_counter.setText(
                f"Кол-во символов: {len(self._desc_text_edit.toPlainText())}"
            )
        )
        root.addWidget(desc_counter)

        if PRIORITIES:
            priority_label = QLabel("Приоритет:")
            root.addWidget(priority_label)
            
            priority_layout = QHBoxLayout()

            self._radio_priorities = []

            for priority in PRIORITIES:
                self._radio_priorities.append(QRadioButton(priority))

            self._radio_priorities[0].setChecked(True)

            for radio_priority in self._radio_priorities:
                priority_layout.addWidget(radio_priority)

            root.addLayout(priority_layout)

        extra_label = QLabel("Дополнительные настройки:")
        root.addWidget(extra_label)

        self._checkbox_complete = QCheckBox("Отметить выполненной")
        root.addWidget(self._checkbox_complete)

        self._checkbox_pin = QCheckBox("Закрепить")
        root.addWidget(self._checkbox_pin)

        button_layout = QHBoxLayout()

        button_clear = QPushButton("Очистить")
        button_clear.clicked.connect(self._on_clear_form)
        button_layout.addWidget(button_clear)

        button_create = QPushButton("Создать")
        button_create.clicked.connect(self._on_create_task)
        button_layout.addWidget(button_create)

        root.addLayout(button_layout)

    def get_task(self, task_id: int) -> Task:
        title = self._title_line_edit.text()
        desc = self._desc_text_edit.toPlainText()
        priority = None

        for i in range(len(PRIORITIES)):
            if self._radio_priorities[i].isChecked():
                priority = PRIORITIES[i]

        is_completed = self._checkbox_complete.isChecked()
        is_pinned = self._checkbox_pin.isChecked()

        return Task(task_id, title, desc, priority, is_completed, is_pinned)