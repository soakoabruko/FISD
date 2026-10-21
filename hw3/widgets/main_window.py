#!/usr/bin/env python3
from itertools import count

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from task import Task
from widgets.about_dialog import AboutDialog
from widgets.constants import PRIORITIES
from widgets.settings_dialog import SettingsDialog
from widgets.task_dialog import TaskDialog
from widgets.task_widget import TaskWidget


class MainWindow(QMainWindow):
    theme_changed = pyqtSignal(str)

    def _on_open_settings(self) -> None:
        dialog = SettingsDialog(self)
        dialog.theme_changed.connect(self.theme_changed.emit)
        dialog.exec()

    def _get_filtered_tasks(self) -> list[Task]:
        key = self._filter.currentText()
        tasks = [*self._pinned_tasks.values(), *self._unpinned_tasks.values()]

        if key == "Все":
            return tasks
        
        return [task for task in tasks if task.priority == key]

    def _on_delete_task(self, task_id: int) -> None:
        self._pinned_tasks.pop(task_id, None)
        self._unpinned_tasks.pop(task_id, None)
        self._refresh_list()

    def _refresh_list(self) -> None:
        self._list.clear()

        filtered_tasks = self._get_filtered_tasks()

        for task in filtered_tasks:
            item = QListWidgetItem(self._list)

            widget = TaskWidget(task)
            widget.deleted.connect(self._on_delete_task)

            item.setSizeHint(widget.sizeHint())
            self._list.setItemWidget(item, widget)

    def _on_create_task(self) -> None:
        dialog = TaskDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            task_id = next(self._task_id_count)
            task = dialog.get_task(task_id)

            if task.is_pinned:
                self._pinned_tasks[task_id] = task
            else:
                self._unpinned_tasks[task_id] = task

            total = len(self._pinned_tasks) + len(self._unpinned_tasks)

            self._counter.setText(f"Кол-во задач: {total}")
            self._refresh_list()

    def __init__(self) -> None:
        super().__init__()
        self._task_id_count = count(1)
        self._pinned_tasks: dict[int, Task] = {}
        self._unpinned_tasks: dict[int, Task] = {}

        self.setWindowTitle("Задачи")
        self.resize(400, 600)

        menu_bar = self.menuBar()

        about_menu = menu_bar.addAction("О программе")
        about_menu.triggered.connect(lambda: AboutDialog(self).exec())

        settings_menu = menu_bar.addAction("Настройки")
        settings_menu.triggered.connect(self._on_open_settings)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)

        self._counter = QLabel("Кол-во задач: 0")
        root.addWidget(self._counter)

        self._filter = QComboBox()
        self._filter.addItems(("Все", *PRIORITIES))
        self._filter.currentTextChanged.connect(self._refresh_list)
        root.addWidget(self._filter)

        self._list = QListWidget()
        root.addWidget(self._list)

        button = QPushButton("Создать новую задачу")
        button.clicked.connect(self._on_create_task)
        root.addWidget(button)