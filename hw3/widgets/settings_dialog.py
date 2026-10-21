#!/usr/bin/env python3
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SettingsDialog(QDialog):
    theme_changed = pyqtSignal(str)

    def __init__(self, parent: QWidget | None=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Настройки")

        root = QVBoxLayout(self)

        theme_layout = QHBoxLayout()
        
        theme_label = QLabel("Тема оформления:")
        theme_layout.addWidget(theme_label)

        dark_theme_button = QPushButton("Темная 🌙")
        dark_theme_button.clicked.connect(lambda: self.theme_changed.emit("dark"))
        theme_layout.addWidget(dark_theme_button)

        light_theme_button = QPushButton("Светлая ☀️")
        light_theme_button.clicked.connect(lambda: self.theme_changed.emit("light"))
        theme_layout.addWidget(light_theme_button)

        root.addLayout(theme_layout)
        