import sys

from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import QMainWindow, QApplication

from UI_Files.AuthWindow_UI import Ui_MainWindow as AuthWin_UI
from UI_Files.RegWindow_UI import Ui_MainWindow as RegWin_UI
from WindowClasses.Admin import AdminWindow
from WindowClasses.User import UserWindow
from WindowClasses.functions import show_message
from database import db


class Auth(QMainWindow, AuthWin_UI):
    def __init__(self):
        super(Auth, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Авторизация')
        self.login_le.setPlaceholderText('Введите логин')
        self.password_le.setPlaceholderText('Введите пароль')

        self.reg_btn.clicked.connect(self.openRegWindow)
        self.auth_btn.clicked.connect(self.login)

        self.db = db
        self.query: QSqlQuery = QSqlQuery(db)

    def openRegWindow(self):
        self.reg = Registration()
        self.reg.show()
        self.hide()

    def login(self):
        user_login = self.login_le.text()
        user_password = self.password_le.text()

        if len(user_login) == 0:
            show_message(self, 'Ошибка', 'Поле логина не должно быть пустым!')
            return

        if len(user_password) == 0:
            show_message(self, 'Ошибка', 'Поле пароля не должно быть пустым!')
            return

        self.query.exec(f'SELECT login, password, role FROM User WHERE login="{user_login}"')
        if self.query.first():
            role = self.query.value(2)
            check_pass = self.query.value(1) == user_password
            if check_pass:
                match role:
                    case 'admin':
                        self.new_window = AdminWindow()
                        self.new_window.show()
                        self.hide()
                    case 'user':
                        self.new_window = UserWindow(user_login)
                        self.new_window.show()
                        self.hide()
                    case _:
                        show_message(self, 'Ошибка', 'Ошибка авторизации!          ')
            else:
                show_message(self, 'Ошибка', 'Неправильный пароль!                 ')
        else:
            show_message(self, 'Ошибка', 'Нет такого пользователя!                 ')


class Registration(QMainWindow, RegWin_UI):
    def __init__(self):
        super(Registration, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Регистрация')
        self.login_le.setPlaceholderText('Введите логин')
        self.password_le.setPlaceholderText('Введите пароль')

        self.auth_btn.clicked.connect(self.openAuthWindow)
        self.reg_btn.clicked.connect(self.reg)

        self.db = db
        self.query: QSqlQuery = QSqlQuery(db)

    def openAuthWindow(self):
        self.reg = Auth()
        self.reg.show()
        self.hide()

    def reg(self):
        user_login = self.login_le.text()
        user_password = self.password_le.text()
        user_role = 'user'

        if len(user_login) == 0:
            show_message(self, 'Ошибка', 'Поле логина не должно быть пустым!')
            return

        if len(user_password) == 0:
            show_message(self, 'Ошибка', 'Поле пароля не должно быть пустым!')
            return

        self.query.exec(f'SELECT login FROM User WHERE login="{user_login}"')
        self.query.first()
        if self.query.value(0) is None:
            self.query.exec(f'INSERT INTO User(login, password, role) '
                            f'VALUES ("{user_login}", "{user_password}", "{user_role}")')

            self.new_window = UserWindow(user_login)
            self.new_window.show()
            self.hide()
        else:
            show_message(self, 'Ошибка', 'Такой пользователь уже зарегистрирован!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Auth()
    main_window.show()
    sys.exit(app.exec())
