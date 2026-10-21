#!/usr/bin/env python3
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget


class AboutDialog(QDialog):
    def __init__(self, parent: QWidget | None=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("О программе")

        root = QVBoxLayout(self)

        content_label = QLabel("Здесь может быть ваша реклама")
        root.addWidget(content_label)