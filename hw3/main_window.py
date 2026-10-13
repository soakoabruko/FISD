#!/usr/bin/env python3
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QComboBox, QPushButton, QDialog,
    QListWidget, QListWidgetItem,
)
from task import Task
from task_widget import TaskWidget
from task_dialog import TaskDialog


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._tasks: list[Task] = []

        self.setWindowTitle("Задачи")
        self.resize(400, 600)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)

        self._filter = QComboBox()
        self._filter.addItems(['Все', 'Низкий', 'Средний', 'Высокий'])
        self._filter.currentTextChanged.connect(self._refresh_list)

        self._list = QListWidget()
        self._refresh_list()

        button = QPushButton("Создать новую задачу")
        button.clicked.connect(self._on_create_task)

        root.addWidget(self._filter)
        root.addWidget(self._list)
        root.addWidget(button)

    def _get_filtered_tasks(self) -> list[Task]:
        key = self._filter.currentText()

        if key == "Все":
            return self._tasks
        
        return [task for task in self._tasks if task.priority == key]

    def _refresh_list(self) -> None:
        self._list.clear()

        filtered_tasks = self._get_filtered_tasks()

        for task in filtered_tasks:
            item = QListWidgetItem(self._list)
            widget = TaskWidget(task)
            item.setSizeHint(widget.sizeHint())
            self._list.setItemWidget(item, widget)


    def _on_create_task(self) -> None:
        dialog = TaskDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            task = dialog.get_task()
            self._tasks.append(task)
            self._refresh_list()