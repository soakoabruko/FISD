#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QRadioButton, QCheckBox, QTextEdit, QPushButton

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("User Profile")
window.resize(400, 600)

central = QWidget()
window.setCentralWidget(central)

form = QVBoxLayout(central)

title = QLabel("Create your profile")

name_layout = QHBoxLayout()
name_label = QLabel("Name:")
name_line_edit = QLineEdit()
name_layout.addWidget(name_label)
name_layout.addWidget(name_line_edit)

age_layout = QHBoxLayout()
age_label = QLabel("Age:")
age_line_edit = QLineEdit()
age_layout.addWidget(age_label)
age_layout.addWidget(age_line_edit)

work_format_title = QLabel("Work format:")

work_format_layout = QHBoxLayout()
office_radio = QRadioButton("Office")
remote_radio = QRadioButton("Remote")
hybrid_radio = QRadioButton("Hybrid")
work_format_layout.addWidget(office_radio)
work_format_layout.addWidget(remote_radio)
work_format_layout.addWidget(hybrid_radio)

checkbox = QCheckBox("Receive notifications")

about_title = QLabel("About:")

about_text_edit = QTextEdit()

button = QPushButton("Create profile")

result_title = QLabel("Result:")

result_text_edit = QTextEdit()

def on_create_profile():
    name = name_line_edit.text()
    age = age_line_edit.text()

    if office_radio.isChecked():
        work_format = "Office"
    elif remote_radio.isChecked():
        work_format = "Remote"
    elif hybrid_radio.isChecked():
        work_format = "Hybrid"
    else:
        work_format = "Not selected"

    notifications = "Yes" if checkbox.isChecked() else "No"
    about = about_text_edit.toPlainText()

    result = f"Name: {name}\nAge: {age}\nWork format: {work_format}\nNotifications: {notifications}\nAbout: {about}"

    result_text_edit.setText(result)

button.clicked.connect(on_create_profile)

form.addWidget(title)
form.addLayout(name_layout)
form.addLayout(age_layout)
form.addWidget(work_format_title)
form.addLayout(work_format_layout)
form.addWidget(checkbox)
form.addWidget(about_title)
form.addWidget(about_text_edit)
form.addWidget(button)
form.addWidget(result_title)
form.addWidget(result_text_edit)

window.show()

sys.exit(app.exec())