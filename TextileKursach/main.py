import sys
from PyQt6.QtWidgets import QApplication
from WindowClasses.Auth import Auth

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Auth()
    main_window.show()
    sys.exit(app.exec())
