from PyQt6.QtWidgets import QMessageBox


def show_message(parent, title, text):
    message = QMessageBox(parent)
    message.setWindowTitle(title)
    message.setText(text)
    message.exec()