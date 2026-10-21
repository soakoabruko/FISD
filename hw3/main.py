#!/usr/bin/env python3
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from widgets.main_window import MainWindow


BASE_DIR = Path(__file__).resolve().parent


def main() -> None:
    app = QApplication(sys.argv)

    def _on_theme_changed(color: str) -> None:
        theme_path = BASE_DIR / "themes" / f"{color}_theme.qss"

        try:
            with open(theme_path, "r", encoding="utf-8") as file:
                app.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Ошибка: Файл темы {theme_path.name} не найден.")

    window = MainWindow()
    window.theme_changed.connect(_on_theme_changed)

    _on_theme_changed("dark")
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()